from typing import Final

import structlog
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from opentelemetry import trace
from opentelemetry.trace import StatusCode
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette.responses import JSONResponse

from taskly.presentation.fast_api.exceptions.constants import error_to_http_status
from taskly.presentation.fast_api.exceptions.responses import InternalServerError, ErrorResponse, \
    IntegrityConflictError, ValidationError
from taskly_common.exceptions import AppError



SERVER_ERROR: Final[int] = 500
logger = structlog.get_logger(__name__)

async def get_app_error_response(
    err: AppError,
) -> JSONResponse:
    try:
        http_status = error_to_http_status[type(err)]
    except KeyError:
        logger.critical(
            "AppError is missing status code mapping",
            error_type=err.__class__.__qualname__
            if not isinstance(err, InternalServerError)
            else err.orig_error.__class__.__qualname__,
        )
        http_status = 500

    error_response = ErrorResponse(
        code=err.code,
        message=err.message,
        meta=err.meta,
    ).model_dump(mode="json")

    if http_status < SERVER_ERROR:
        logger.info("Handled error", error_response=error_response, exc_info=err)
    else:
        logger.error("Unexpected error", exc_info=err)

    return JSONResponse(
        status_code=http_status,
        content=error_response,
    )


async def app_error_handler(_request: Request, exc: Exception) -> JSONResponse:

    span = trace.get_current_span()
    span.record_exception(exc)
    app_error = exc if isinstance(exc, AppError) else None
    if app_error is None and isinstance(exc, IntegrityError):
        logger.info("Handling database integrity conflict", exc_info=exc)
        app_error = IntegrityConflictError(orig_error=exc)
    if app_error is None:
        logger.exception("Handling unexpected internal server error", exc_info=exc)
        span.set_status(StatusCode.ERROR, str(exc))
        app_error = InternalServerError(orig_error=exc)
    return await get_app_error_response(app_error)


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return await app_error_handler(
        request,
        ValidationError(details=jsonable_encoder({"detail": exc.errors(), "body": exc.body})),
    )