from typing import ClassVar

from taskly_common.exceptions import app_error, AppError


@app_error
class EmailVerificationCodeNotFound(AppError):
    code: ClassVar[str] = "VERIFICATION_CODE_NOT_FOUND"
    message: str = "Email verification code not found"

@app_error
class EmailVerificationCodeDoesntMatch(AppError):
    code: ClassVar[str] = "VERIFICATION_CODE_ERROR"
    message: str = "Email verification code doesn't match"