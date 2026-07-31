from fastapi import FastAPI, APIRouter

from taskly.presentation.fast_api.routers.v1.general import root_router


def include_routers_api_v1(app: FastAPI) -> None:
    api_v1_router = APIRouter(prefix="/v1")

    api_v1_router.include_router(root_router)

    app.include_router(api_v1_router)

__all__ = [
    "include_routers_api_v1",
]