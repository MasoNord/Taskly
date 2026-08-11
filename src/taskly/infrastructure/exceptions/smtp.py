from typing import ClassVar, Any

from taskly_common.exceptions import AppError, app_error


@app_error
class SMTPServerTimeoutError(AppError):
    code: ClassVar[str] = "SERVICE_UNAVAILABLE"
    message: str = "SMTP server unavailable due to timeout error"
    orig_error: Exception

    @property
    def meta(self) -> dict[str, Any] | None:
        return {"orig_error": str(self.orig_error)}