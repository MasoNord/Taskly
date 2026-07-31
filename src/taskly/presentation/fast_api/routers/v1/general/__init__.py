from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from taskly.presentation.fast_api.routers.v1.general.alive import create_alive_router

root_router = APIRouter(
    tags=["Root"],
    route_class=DishkaRoute
)

root_router.include_router(create_alive_router())

__all__ = [
    "root_router"
]