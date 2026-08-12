from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LocalDBConnectionConfig:
    postgres_username: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_database: str

    @property
    def postgres_conn_url(self) -> str:
        user = self.postgres_username
        password = self.postgres_password
        host = self.postgres_host
        port = self.postgres_port
        db_name = self.postgres_database

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


@dataclass(frozen=True, slots=True)
class EngineSettings:
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int
