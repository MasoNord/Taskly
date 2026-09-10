import uuid
from dataclasses import dataclass
from logging import Logger

import structlog

from taskly.application.common.gateway.email_sender import EmailSenderGateway, EmailVerificationCodeTemplate
from taskly.application.common.gateway.email_verification_code_storage import EmailVerificationCodeStorage, EmailVerificationCodeRequest
from taskly.application.common.gateway.uow import UoW
from taskly.application.common.gateway.user import UserGateway
from taskly.application.common.service.email_verification_code_generator import EmailVerificationCodeGenerator
from taskly.application.common.service.email_verification_code_url_generator import EmailVerificationCodeUrlGenerator
from taskly.application.exceptions.email_verification_code_storage import EmailVerificationCodeNotFound, \
    EmailVerificationCodeDoesntMatch
from taskly.domain.entities.user import User
from taskly.infrastructure.auth.session.service import AuthSessionService
from taskly.infrastructure.exceptions.auth import AuthenticationError, AlreadyAuthenticatedError
from taskly_common.hasher import sign, verify
from taskly_common.interactors import interactor

logger: Logger = structlog.get_logger(__name__)

@dataclass
class VerifyEmailVerificationCodeRequest:
    user_agent: str | None
    ip_address: str | None
    email: str
    verification_code: str

@dataclass
class VerifyEmailVerificationCodeResponse:
    user_id: uuid.UUID
    email: str

@interactor
class GetEmailVerificationCodeUrl:

    _email_verification_code_generator: EmailVerificationCodeGenerator
    _email_verification_code_url_generator: EmailVerificationCodeUrlGenerator
    _email_verification_code_storage: EmailVerificationCodeStorage
    _email_sender_gateway: EmailSenderGateway

    async def execute(self, email: str) -> str:
        logger.info("Generating verification code url for email: %s", email)

        code = await self._email_verification_code_generator.generate_verification_code()

        url = await self._email_verification_code_url_generator.generate(email)

        logger.debug("Verification code url: %s", url)

        email_verification_code_request = EmailVerificationCodeRequest(
            email=email,
            hashed_code=sign(code.encode("utf-8")),
        )

        # TODO: add sending notification to the user by the given email via event bus

        email_request = EmailVerificationCodeTemplate(
            context = {"verification_code": code}
        )

        await self._email_verification_code_storage.add(email_verification_code_request)

        await self._email_sender_gateway.send(
            email,
            email_request.subject,
            email_request.template_name,
            dict(email_request.context)
        )

        logger.info("End generating verification code url")

        return url

@interactor
class VerifyEmailVerificationCode:

    _uow: UoW
    _user_gateway: UserGateway
    _auth_session: AuthSessionService
    _email_verification_code_storage: EmailVerificationCodeStorage
    _email_verification_code_generator: EmailVerificationCodeGenerator

    async def execute(self, request: VerifyEmailVerificationCodeRequest) -> VerifyEmailVerificationCodeResponse:
        logger.info("Start verifying email verification code")

        email_request = await self._email_verification_code_storage.get_by_email(request.email)

        if not email_request:
            logger.info("Email verification code not found for email: %s", request.email)
            raise EmailVerificationCodeNotFound

        if not verify(request.verification_code.encode('utf-8'), email_request.hashed_code):
            raise EmailVerificationCodeDoesntMatch

        user = await self._user_gateway.get_by_email(request.email)

        if not user:
            user = User(
                id=uuid.uuid7(),
                email=request.email,
                first_name=None,
                last_name=None,
                patronymic=None,
                username=None,
                last_login_at=None,
            )
            await self._user_gateway.add(user)

        try:
            await self._auth_session.get_authenticated_user_id()
            raise AlreadyAuthenticatedError
        except AuthenticationError:
            pass

        await self._auth_session.issue_session(
            user.id,
            request.user_agent,
            request.ip_address
        )

        await self._uow.commit()

        return VerifyEmailVerificationCodeResponse(
            user_id=user.id,
            email=request.email,
        )



