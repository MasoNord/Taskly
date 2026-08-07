
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from taskly.domain.entities.auth_session import AuthSession
from taskly.infrastructure.auth.session.gateway.auth_session import AuthSessionGateway


class SAAuthSessionGateway(AuthSessionGateway):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, auth_session: AuthSession) -> None:
        self._session.add(auth_session)


    async def get_by_id(self, auth_session_id: str) -> AuthSession | None:
        stmt = select(AuthSession).where(AuthSession.id_ == auth_session_id) # type: ignore

        record = await self._session.execute(stmt)

        result = record.scalar_one_or_none()

        return result

    async def update(self, auth_session: AuthSession) -> None:
        pass

    async def delete(self, auth_session_id: str) -> None:
        pass

    async def delete_all_for_user(self, user_id: UUID) -> None:
        pass
