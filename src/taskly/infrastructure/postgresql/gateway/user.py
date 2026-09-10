from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from taskly.application.common.gateway.user import UserGateway
from taskly.domain.entities.user import User
from taskly.presentation.fast_api.exceptions.responses import InternalServerError


class SAUserGateway(UserGateway):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user: User) -> None:
        try:
            self.session.add(user)
            await self.session.flush((user,))
        except SQLAlchemyError as err:
            raise InternalServerError(orig_error=err)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).filter_by(email=email)
        record = await self.session.execute(stmt)
        return record.scalar_one_or_none()