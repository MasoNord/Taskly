from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from taskly.bootstrap.config_loader import Config
from taskly.bootstrap.di.container import get_async_container
from taskly.presentation.fast_api.routers import include_routers_api_v1


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    container: AsyncContainer = app.state.dishka_container
    yield
    await container.close()


def create_app(config: Config) -> FastAPI:

    app = FastAPI(
        lifespan=lifespan,
        root_path=config.api.root_path,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors.allow_origins,
        allow_credentials=config.cors.allow_credentials,
        allow_methods=config.cors.allow_methods,
        allow_headers=config.cors.allow_headers,
    )
    container = get_async_container(config)
    setup_dishka(container=container, app=app)

    include_routers_api_v1(app)

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
        # log_config=log_config,
    )

if __name__ == "__main__":
    run_api()