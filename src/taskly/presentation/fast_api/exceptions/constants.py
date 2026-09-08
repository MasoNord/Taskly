from taskly.application.exceptions.email_verification_code_storage import EmailVerificationCodeNotFound, \
    EmailVerificationCodeDoesntMatch
from taskly.infrastructure.exceptions.smtp import SMTPServerTimeoutError
from taskly_common.exceptions import AppError




error_to_http_status: dict[type[AppError], int] = {
    SMTPServerTimeoutError: 503,
    EmailVerificationCodeNotFound: 404,
    EmailVerificationCodeDoesntMatch: 400
}