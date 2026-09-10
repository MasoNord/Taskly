from typing import ClassVar

from taskly_common.exceptions import AppError, app_error


@app_error
class AuthenticationError(AppError):
    message: str = "Authentication Error"
    code: ClassVar[str] = "AUTHENTICATION_ERROR"

@app_error
class AlreadyAuthenticatedError(AppError):
    message: str = "User already authenticated error"
    code: ClassVar[str] = "USER_ALREADY_AUTHENTICATED_ERROR"

@app_error
class ReAuthenticationError(AppError):
    message: str = "Re authentication error"
    code: ClassVar[str] = "RE_AUTHENTICATION_ERROR"

@app_error
class AuthenticationChangeError(AppError):
    message: str = "Authentication change error"
    code: ClassVar[str] = "AUTHENTICATION_CHANGE_ERROR"