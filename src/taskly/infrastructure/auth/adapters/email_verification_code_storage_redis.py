from typing import override

from taskly.application.common.gateway.email_verification_code_storage import EmailVerificationCodeStorage, \
    EmailVerificationCodeRequest


class RedisEmailVerificationCodeStorage(EmailVerificationCodeStorage):

    @override
    async def add(self, request: EmailVerificationCodeRequest) -> None:
        pass