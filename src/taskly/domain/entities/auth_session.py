from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class AuthSession:
    id: str
    user_id: UUID
    ip_address: str | None
    user_agent: str | None
    expiration: datetime
    created_at: datetime