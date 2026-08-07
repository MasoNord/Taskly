from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    id: UUID
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    username: str | None
    email: str
    last_login_at: datetime | None