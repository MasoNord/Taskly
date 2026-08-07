from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from taskly.domain.entities.auth_session import AuthSession


class AuthSessionGateway(Protocol):

    @abstractmethod
    async def add(self, auth_session: AuthSession) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, auth_session_id: str) -> AuthSession | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, auth_session: AuthSession) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, auth_session_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_all_for_user(self, user_id: UUID) -> None:
        raise NotImplementedError
