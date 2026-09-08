from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

@dataclass
class EmailVerificationCodeRequest:
    email: str
    hashed_code: bytes

@dataclass
class EmailVerificationCodeResponse:
    hashed_code: bytes

class EmailVerificationCodeStorage(Protocol):

    @abstractmethod
    async def add(self, request: EmailVerificationCodeRequest) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> EmailVerificationCodeResponse | None:
        raise NotImplementedError
