from dataclasses import dataclass
from typing import Literal


@dataclass(slots=True, frozen=True)
class AuthConfig:
    secret_key: str
    session_ttl_min: int
    session_refresh_threshold: float

@dataclass(frozen=True, slots=True)
class CookiesConfig:
    secure: bool
    samesite: Literal["strict", "lax", "none"]
