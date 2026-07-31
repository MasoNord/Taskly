from fastapi import APIRouter
from fastapi.responses import JSONResponse


def create_alive_router() -> APIRouter:
    router = APIRouter()

    @router.get("/internal/alive")
    async def alive() -> JSONResponse:
        return JSONResponse(status_code=200, content={"status": "ok"})


    return router
