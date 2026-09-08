from dishka import AsyncContainer, make_async_container, STRICT_VALIDATION

from taskly.bootstrap.config_loader import Config
from taskly.bootstrap.configs.database_config import LocalDBConnectionConfig, EngineSettings
from taskly.bootstrap.configs.email_config import EmailConnectionConfig, EmailTemplateRendererConfig
from taskly.bootstrap.configs.redis_config import RedisConfig, RedisExpirationConfig
from taskly.bootstrap.configs.server_config import ServerConfig, ApiConfig
from taskly.bootstrap.di.providers.application import application_providers
from taskly.bootstrap.di.providers.infrastructure import infrastructure_providers


def get_async_container(config: Config) -> AsyncContainer:

    providers = [
        *infrastructure_providers(),
        *application_providers()
    ]

    context = {
        Config: config,
        ServerConfig: config.server,
        ApiConfig: config.api,
        RedisConfig: config.redis_config,
        LocalDBConnectionConfig: config.postgres,
        EngineSettings: config.engine_settings,
        EmailConnectionConfig: config.email_connection,
        EmailTemplateRendererConfig: config.email_template_render,
        RedisExpirationConfig: config.redis_expiration_config
    }

    container = make_async_container(*providers, context=context, validation_settings=STRICT_VALIDATION)

    return container