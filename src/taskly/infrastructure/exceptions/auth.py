from taskly_common.exceptions import AppError, app_error


@app_error
class AuthenticationError(AppError):
    message: str

@app_error
class AlreadyAuthenticatedError(AppError):
    pass

@app_error
class ReAuthenticationError(AppError):
    pass

@app_error
class AuthenticationChangeError(AppError):
    pass