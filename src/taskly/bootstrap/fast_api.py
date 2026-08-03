from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


from taskly.bootstrap.config_loader import Config
from taskly.bootstrap.di.container import get_async_container
from taskly.presentation.fast_api.middlewares import include_middlewares
from taskly.presentation.fast_api.routers import include_routers_api_v1
from taskly_common.logs import configure_structlog
from taskly_common.observability.setup import setup_observability

log_config = configure_structlog()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    container: AsyncContainer = app.state.dishka_container
    yield
    await container.close()


def create_app(config: Config) -> FastAPI:

    setup_observability(config.otel)

    app = FastAPI(
        lifespan=lifespan,
        root_path=config.api.root_path,
    )

    FastAPIInstrumentor.instrument_app(
        app,
        excluded_urls="/internal/alive,/internal/ready",
    )

    container = get_async_container(config)
    setup_dishka(container=container, app=app)

    include_routers_api_v1(app)
    include_middlewares(app, cors_config=config.cors)

    return app

def app_factory() -> FastAPI:
    return create_app(Config.load())

def run_api() -> None:

    config = Config.load()
    uvicorn.run(
        "taskly.bootstrap.fast_api:app_factory",
        factory=True,
        port=config.server.port,
        host=config.server.host,
        workers=config.server.workers,
        log_config=log_config,
    )

if __name__ == "__main__":
    run_api()