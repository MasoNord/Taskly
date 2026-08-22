from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from taskly.presentation.fast_api.routers.v1.general.alive import create_alive_router, create_ready_router, \
    create_ready_redis_router

root_router = APIRouter(
    tags=["Root"]
)

root_router.include_router(create_alive_router())
root_router.include_router(create_ready_router())
root_router.include_router(create_ready_redis_router())

__all__ = [
    "root_router"
]