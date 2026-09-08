from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from pydantic import BaseModel, EmailStr
from starlette.responses import RedirectResponse

from starlette.status import HTTP_307_TEMPORARY_REDIRECT, HTTP_200_OK

from taskly.infrastructure.auth.handlers.sign_up_via_email import GetEmailVerificationCodeUrl, \
    VerifyEmailVerificationCode


class VerifyVerificationCodeRequestPydantic(BaseModel):
    verification_code: str
    email: EmailStr

def create_get_verification_email_code_url_router() -> APIRouter:

    router = APIRouter()

    @router.get(
        "/signup/email/verification-code",
        status_code=HTTP_307_TEMPORARY_REDIRECT,
        description="Generates verification code and send it to user via requested email"
    )
    @inject
    async def get_verification_code_url(
        interactor: FromDishka[GetEmailVerificationCodeUrl],
        email: EmailStr = Query()
    ):

        url = await interactor.execute(email)

        return RedirectResponse(
            url=url
        )

    return router

def create_get_verify_email_code_router() -> APIRouter:

    router = APIRouter()

    @router.post(
        "/signup/email/verification-code",
        status_code=HTTP_200_OK,
        description="Verifies verification code"
    )
    @inject
    async def verify_verification_code(
        interactor: FromDishka[VerifyEmailVerificationCode],
        payload: VerifyVerificationCodeRequestPydantic
    ):
        return await interactor.execute(payload.email, payload.verification_code)

    return router