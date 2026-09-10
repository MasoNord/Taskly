from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from taskly.application.common.gateway.uow import UoW

class BaseSQLAlchemyUoW(UoW):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self._session.rollback()

    async def flush(self, objects: Sequence[Any] | None = None) -> None:
        await self._session.flush(objects)


    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()