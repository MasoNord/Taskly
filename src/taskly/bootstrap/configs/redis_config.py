

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RedisConfig:
    max_connections: int
    port: int
    host: str
    decode_response: bool
    acl_password: str
    acl_username: str

    @property
    def redis_conn_url(self) -> str:
        return f"redis://{self.acl_username}:{self.acl_password}@{self.host}:{self.port}"

@dataclass(frozen=True, slots=True)
class RedisExpirationConfig:

    email_verification_code_ex: int
