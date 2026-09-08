from typing import override, Final

from redis.asyncio import Redis

from taskly.application.common.gateway.email_verification_code_storage import EmailVerificationCodeStorage, \
    EmailVerificationCodeRequest
from taskly.bootstrap.configs.redis_config import RedisExpirationConfig

KEY_NAME_PREFIX: Final[str] = "email:verification-code"

class RedisEmailVerificationCodeStorage(EmailVerificationCodeStorage):

    def __init__(self, redis: Redis, redis_expiration_conf: RedisExpirationConfig) -> None:
        self._redis = redis
        self._redis_expiration_conf = redis_expiration_conf

    @override
    async def add(self, request: EmailVerificationCodeRequest) -> None:

        await self._redis.set(
            name=f"{KEY_NAME_PREFIX}:{request.email}",
            ex=self._redis_expiration_conf.email_verification_code_ex,
            value=request.hashed_code
        )