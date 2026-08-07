from taskly_common.exceptions import app_error, AppError


@app_error
class RedisConnectionError(AppError):
    pass