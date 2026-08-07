from datetime import UTC, datetime
from typing import Final
from uuid import UUID

import structlog

from taskly.application.common.gateway.uow import UoW
from taskly.domain.entities.auth_session import AuthSession
from taskly.infrastructure.auth.session.gateway.auth_session import AuthSessionGateway
from taskly.infrastructure.auth.session.gateway.transport import AuthSessionTransport
from taskly.infrastructure.auth.session.id_generator_str import StrAuthSessionIdGenerator
from taskly.infrastructure.auth.session.timer_utc import UtcAuthSessionTimer
from taskly.infrastructure.exceptions.auth import AuthenticationError

logger = structlog.get_logger(__name__)

AUTH_UNAVAILABLE: Final[str] = (
    "Authentication is currently unavailable. Please try again later."
)
AUTH_NOT_AUTHENTICATED: Final[str] = "Not authenticated."
AUTH_SESSION_EXPIRED: Final[str] = "Auth session expired."
AUTH_SESSION_EXTENSION_FAILED: Final[str] = "Auth session extension failed."
AUTH_SESSION_EXTRACTION_FAILED: Final[str] = "Auth session extraction failed."
AUTH_SESSION_NOT_FOUND: Final[str] = "Auth session not found."

class AuthSessionService:

    def __init__(
            self,
            auth_session_gateway: AuthSessionGateway,
            auth_session_transport: AuthSessionTransport,
            auth_session_id_generator: StrAuthSessionIdGenerator,
            auth_session_timer: UtcAuthSessionTimer,
            uow: UoW,
    ) -> None:
        self._auth_session_gateway = auth_session_gateway
        self._auth_session_transport = auth_session_transport
        self._main_uow = uow
        self._auth_session_timer = auth_session_timer
        self._auth_session_id_generator = auth_session_id_generator

    async def issue_session(self, user_id: UUID, user_agent: str, ip: str) -> None:
        """:raises AuthenticationError:"""
        logger.debug("Issue auth session: started. User ID: '%s'.", user_id)
        logger.debug("User-Agent: %s", user_agent)
        logger.debug("IP: %s", ip)

        auth_session_id: str = self._auth_session_id_generator.generate()
        expiration: datetime = self._auth_session_timer.auth_session_expiration
        auth_session = AuthSession(
            id=auth_session_id,
            user_id=user_id,
            expiration=expiration,
            ip_address=ip,
            user_agent=user_agent,
            created_at=datetime.now(tz=UTC),
        )

        await self._auth_session_gateway.add(auth_session)

        self._auth_session_transport.deliver(auth_session)

        logger.debug(
            "Issue auth session: done. User ID: '%s', Auth session ID: '%s'.",
            user_id,
            auth_session.id,
        )

    async def terminate_current_session(self) -> None:

        auth_session_id = self._auth_session_transport.extract_id()
        if auth_session_id is None:
            logger.warning(
                "Terminate current session failed: partially failed. "
                "Session ID can't be extracted from transport. "
                "Auth session can't be identified.",
            )
            return
        logger.debug(
            "Terminate current session: using ID from transport. "
            "Auth session ID: '%s'.",
            auth_session_id,
        )

        self._auth_session_transport.remove_current()

        await self._auth_session_gateway.delete(auth_session_id)
        logger.debug(
            "Terminate current session: done (transport cleared, storage deleted). "
            "Auth session ID: '%s'.",
            auth_session_id,
        )

    async def get_authenticated_user_id(self) -> UUID:
        """:raises AuthenticationError:"""
        logger.debug("Get authenticated user ID: started.")

        raw_auth_session = await self._get_current_auth_session()
        valid_auth_session = await self._validate_and_extend_session(raw_auth_session)

        logger.debug (
            "Get authenticated user ID: done. Auth session ID: '%s'. User ID: '%s'.",
            valid_auth_session.id,
            valid_auth_session.user_id,
        )
        return valid_auth_session.user_id

    async def _get_current_auth_session(self) -> AuthSession:
        """:raises AuthenticationError:"""
        logger.debug("Get current auth session: started. Auth session ID: unknown.")

        auth_session_id: str | None = self._auth_session_transport.extract_id()
        if auth_session_id is None:
            logger.debug(AUTH_SESSION_NOT_FOUND)
            self._auth_session_transport.remove_current()
            raise AuthenticationError(message=AUTH_NOT_AUTHENTICATED)
        logger.debug(
            "Get current auth session: reading from storage. Auth session ID: '%s'.",
            auth_session_id,
        )

        auth_session: (AuthSession | None) = await self._auth_session_gateway.get_by_id(auth_session_id)


        if auth_session is None:
            logger.debug(AUTH_SESSION_NOT_FOUND)
            self._auth_session_transport.remove_current()
            await self._auth_session_gateway.delete(auth_session_id)
            raise AuthenticationError(message=AUTH_NOT_AUTHENTICATED)

        logger.debug(
            "Get current auth session: done. Auth session ID: '%s'.", auth_session.id,
        )
        return auth_session

    async def _validate_and_extend_session(
            self,
            auth_session: AuthSession,
    ) -> AuthSession:
        """:raises AuthenticationError:"""
        logger.debug(
            "Validate and extend auth session: started. Auth session ID: '%s'.",
            auth_session.id,
        )

        now = self._auth_session_timer.current_time
        if auth_session.expiration <= now:
            logger.debug(AUTH_SESSION_EXPIRED)
            raise AuthenticationError(message=AUTH_NOT_AUTHENTICATED)

        if (
                auth_session.expiration - now
                > self._auth_session_timer.refresh_trigger_interval
        ):
            logger.debug(
                "Validate and extend auth session: validated without extension. "
                "Auth session ID: '%s'.",
                auth_session.id,
            )
            return auth_session

        original_expiration = auth_session.expiration
        auth_session.expiration = self._auth_session_timer.auth_session_expiration

        await self._auth_session_gateway.update(auth_session)

        self._auth_session_transport.deliver(auth_session)

        logger.debug(
            "Validate and extend auth session: done. "
            "Auth session ID: '%s'. New expiration: '%s'.",
            auth_session.id,
            auth_session.expiration.isoformat(),
        )
        return auth_session
