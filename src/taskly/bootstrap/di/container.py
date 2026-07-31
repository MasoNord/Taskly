from dishka import AsyncContainer, make_async_container, STRICT_VALIDATION

from taskly.bootstrap.config_loader import Config
from taskly.bootstrap.configs.server_config import ServerConfig, ApiConfig


def get_async_container(config: Config) -> AsyncContainer:

    providers = [

    ]

    context = {
        Config: config,
        ServerConfig: config.server,
        ApiConfig: config.api
    }

    container = make_async_container(*providers, context=context, validation_settings=STRICT_VALIDATION)

    return container