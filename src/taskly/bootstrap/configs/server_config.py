from dataclasses import dataclass


@dataclass(slots=True, frozen=True, kw_only=True)
class ServerConfig:
    host: str
    port: int
    workers: int

@dataclass(slots=True, frozen=True, kw_only=True)
class CorsConfig:

    allow_origins: list[str]
    allow_credentials: bool
    allow_methods: list[str]
    allow_headers: list[str]


@dataclass(slots=True, frozen=True, kw_only=True)
class ApiConfig:

    root_path: str
