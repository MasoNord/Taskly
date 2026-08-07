from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from taskly.presentation.fast_api.exceptions.handlers import app_error_handler, validation_error_handler

def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)


__all__ = [
    "include_exception_handlers",
]