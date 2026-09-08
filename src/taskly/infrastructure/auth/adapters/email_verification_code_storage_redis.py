import json
from typing import override, Final

from redis.asyncio import Redis

from taskly.application.common.gateway.email_verification_code_storage import EmailVerificationCodeStorage, \
    EmailVerificationCodeRequest, EmailVerificationCodeResponse
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

    @override
    async def get_by_email(self, email: str) -> EmailVerificationCodeResponse | None:
        raw_data = await self._redis.get(name=f"{KEY_NAME_PREFIX}:{email}")

        if not raw_data:
            return None

        return EmailVerificationCodeResponse(
            hashed_code=str(raw_data).encode('utf-8'),
        )