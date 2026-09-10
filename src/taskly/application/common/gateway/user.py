from abc import abstractmethod
from typing import Protocol

from taskly.domain.entities.user import User


class UserGateway(Protocol):

    @abstractmethod
    async def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

