from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from starlette.responses import RedirectResponse

from starlette.status import HTTP_307_TEMPORARY_REDIRECT

from taskly.infrastructure.auth.handlers.sign_up_via_email import GetEmailVerificationCodeUrl

class VerificationCodeRequestPydantic(BaseModel):
    email: EmailStr

def create_get_verification_email_code_url_router() -> APIRouter:

    router = APIRouter()

    @router.post(
        "/signup/email/verification-code",
        status_code=HTTP_307_TEMPORARY_REDIRECT,
        description="Generate verification code and send it to user via requested email"
    )
    @inject
    async def get_verification_code_url(
        interactor: FromDishka[GetEmailVerificationCodeUrl],
        payload: VerificationCodeRequestPydantic
    ):

        url = await interactor.execute(payload.email)

        return RedirectResponse(
            url=url
        )

    return router