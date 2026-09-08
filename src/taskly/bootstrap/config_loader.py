import os
from dataclasses import dataclass
from pathlib import Path
from typing import Self, Any

import toml_rs

from taskly.bootstrap.configs.database_config import EngineSettings, LocalDBConnectionConfig
from taskly.bootstrap.configs.email_config import EmailConnectionConfig, EmailTemplateRendererConfig
from taskly.bootstrap.configs.redis_config import RedisConfig, RedisExpirationConfig
from taskly.bootstrap.configs.server_config import ServerConfig, ApiConfig, CorsConfig
from taskly_common.observability.config import OTelConfig

_CONFIG_PATH_ENV = "APP_CONFIG_PATH"

@dataclass(frozen=True, slots=True, kw_only=True)
class Config:

    server: ServerConfig
    api: ApiConfig
    cors: CorsConfig
    otel: OTelConfig
    redis_config: RedisConfig
    redis_expiration_config: RedisExpirationConfig
    engine_settings: EngineSettings
    postgres: LocalDBConnectionConfig
    email_connection: EmailConnectionConfig
    email_template_render: EmailTemplateRendererConfig

    @classmethod
    def load(cls) -> Self:
        config_path = os.environ.get(_CONFIG_PATH_ENV)

        if config_path is None:
            msg = f"'{_CONFIG_PATH_ENV}' must point at the main app TOML config"
            raise RuntimeError(msg)

        with Path(config_path).open("rb") as f:
            data = toml_rs.load(f)

        return cls(
            server=ServerConfig(**data["server"]),
            api=ApiConfig(**data["api"]),
            cors=CorsConfig(**data["cors"]),
            otel=OTelConfig(**data["otel"]),
            engine_settings=EngineSettings(**data["engine_settings"]),
            postgres=LocalDBConnectionConfig(**data["postgres"]),
            redis_config=RedisConfig(**data["redis_config"]),
            email_connection=EmailConnectionConfig(**data["email_connection"]),
            email_template_render=EmailTemplateRendererConfig(**data["email_template_render"]),
            redis_expiration_config=RedisExpirationConfig(**data["redis_expiration_config"])
        )
