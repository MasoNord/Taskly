import structlog
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis

logger = structlog.get_logger(__name__)

def create_alive_router() -> APIRouter:
    router = APIRouter()

    @router.get("/internal/alive")
    async def alive() -> JSONResponse:
        return JSONResponse(status_code=200, content={"status": "ok"})


    return router

def create_ready_router() -> APIRouter:

    router = APIRouter()

    @router.get("/internal/ready")
    @inject
    async def ready(
        session: FromDishka[AsyncSession],
    ) -> JSONResponse:
        """HTTP endpoint for readiness probe."""
        try:
            await session.execute(text("SELECT 1"))
        except Exception as e:  # noqa: BLE001
            await logger.awarning("Database is not ready", exc_info=e)
            return JSONResponse(status_code=503, content={})

        return JSONResponse(status_code=200, content={})

    return router

def create_ready_redis_router() -> APIRouter:

    router = APIRouter()

    @router.get("/internal/redis/ready")
    @inject
    async def ready(
        session: FromDishka[aioredis.Redis]
    ) -> JSONResponse:
        try:
            response = await session.ping()
        except Exception as e:
            await logger.awarning("Redis is not ready", exec_info=e)
            return JSONResponse(status_code=503, content={})

        return JSONResponse(status_code=200, content={"message": response})

    return router


