from logging import Logger

import structlog

from taskly.application.common.gateway.email_sender import EmailSenderGateway, EmailVerificationCodeTemplate
from taskly.application.common.gateway.email_verification_code_storage import EmailVerificationCodeStorage, EmailVerificationCodeRequest
from taskly.application.common.service.email_verification_code_generator import EmailVerificationCodeGenerator
from taskly.application.common.service.email_verification_code_url_generator import EmailVerificationCodeUrlGenerator
from taskly.application.exceptions.email_verification_code_storage import EmailVerificationCodeNotFound, \
    EmailVerificationCodeDoesntMatch
from taskly_common.hasher import sign, verify
from taskly_common.interactors import interactor

logger: Logger = structlog.get_logger(__name__)

@interactor
class GetEmailVerificationCodeUrl:

    _email_verification_code_generator: EmailVerificationCodeGenerator
    _email_verification_code_url_generator: EmailVerificationCodeUrlGenerator
    _email_verification_code_storage: EmailVerificationCodeStorage
    _email_sender_gateway: EmailSenderGateway

    async def execute(self, email: str) -> str:
        logger.info("Generating verification code url for email: %s", email)

        code = await self._email_verification_code_generator.generate_verification_code()

        url = await self._email_verification_code_url_generator.generate(email)

        logger.debug("Verification code url: %s", url)

        email_verification_code_request = EmailVerificationCodeRequest(
            email=email,
            hashed_code=sign(code.encode("utf-8")),
        )

        # TODO: add sending notification to the user by the given email via event bus

        email_request = EmailVerificationCodeTemplate(
            context = {"verification_code": code}
        )

        await self._email_verification_code_storage.add(email_verification_code_request)

        await self._email_sender_gateway.send(
            email,
            email_request.subject,
            email_request.template_name,
            dict(email_request.context)
        )

        logger.info("End generating verification code url")

        return url

@interactor
class VerifyEmailVerificationCode:

    _email_verification_code_storage: EmailVerificationCodeStorage
    _email_verification_code_generator: EmailVerificationCodeGenerator

    async def execute(self, email: str, verification_code: str) -> str:
        logger.info("Start verifying email verification code")

        email_request = await self._email_verification_code_storage.get_by_email(email)

        if not email_request:
            logger.info("Email verification code not found for email: %s", email)
            raise EmailVerificationCodeNotFound

        if not verify(verification_code.encode('utf-8'), email_request.hashed_code):
            raise EmailVerificationCodeDoesntMatch

        return "Success"



