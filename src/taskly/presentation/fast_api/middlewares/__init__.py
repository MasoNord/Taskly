from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from taskly.bootstrap.configs.server_config import CorsConfig
from taskly.presentation.fast_api.middlewares.tracing import tracing_middleware


def include_middlewares(app: FastAPI, cors_config: CorsConfig) -> None:

    app.middleware("http")(tracing_middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_config.allow_origins,
        allow_credentials=cors_config.allow_credentials,
        allow_methods=cors_config.allow_methods,
        allow_headers=cors_config.allow_headers,
    )
    app.add_middleware()

__all__ = [
    "include_middlewares"
]