from taskly.infrastructure.exceptions.smtp import SMTPServerTimeoutError
from taskly_common.exceptions import AppError




error_to_http_status: dict[type[AppError], int] = {
    SMTPServerTimeoutError: 503
}