from fastapi import APIRouter

from taskly.presentation.fast_api.routers.v1.auth.sign_up_via_email import create_get_verification_email_code_url_router

auth_router = APIRouter(prefix="/auth", tags=["Auth specific"])

auth_router.include_router(create_get_verification_email_code_url_router())

__all__ = [
    "auth_router"
]