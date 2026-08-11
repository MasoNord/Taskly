


from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, TypedDict


class EmailVerificationCodeContext(TypedDict):
    verification_code: str

@dataclass(frozen=True, slots=True, kw_only=True)
class EmailVerificationCodeTemplate:
    subject: str = "Code Verification"
    template_name = "verification_code_page.html"
    context: EmailVerificationCodeContext

class EmailSenderGateway(Protocol):

    @abstractmethod
    async def send(self, to: str, subject: str, template_name: str, context: dict) -> None:
        raise NotImplementedError
