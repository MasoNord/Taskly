from logging import Logger

import structlog

from taskly.application.common.gateway.email_sender import EmailSenderGateway, EmailVerificationCodeTemplate
from taskly.application.common.gateway.email_verification_code_storage import EmailVerificationCodeStorage, EmailVerificationCodeRequest
from taskly.application.common.service.email_verification_code_generator import EmailVerificationCodeGenerator
from taskly.application.common.service.email_verification_code_url_generator import EmailVerificationCodeUrlGenerator
from taskly_common.hasher import sign
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


        (url, url_code) = await self._email_verification_code_url_generator.generate()

        logger.debug("Verification code url: %s", url)
        logger.debug("Verification code temp url code: %s", url_code)

        email_verification_code_request = EmailVerificationCodeRequest(
            email=email,
            hashed_code=sign(code.encode("utf-8")),
            url_code=url_code
        )

        # TODO: add sending notification to the user by the given email via event bus

        email_request = EmailVerificationCodeTemplate(
            context = {"verification_code": code}
        )

        await self._email_sender_gateway.send(
            email,
            email_request.subject,
            email_request.template_name,
            dict(email_request.context)
        )

        logger.info("SENDING USE'S VERIFICATION CODE TO THE CONSOLE: %s", code)

        await self._email_verification_code_storage.add(email_verification_code_request)

        logger.info("End generating verification code url")

        return url