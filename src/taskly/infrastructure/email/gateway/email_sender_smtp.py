
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Final

import aiosmtplib
from aiosmtplib import SMTPConnectTimeoutError

from taskly.application.common.gateway.email_sender import EmailSenderGateway
from taskly.bootstrap.configs.email_config import EmailConnectionConfig
from taskly.infrastructure.email.template_renderer import TemplateRenderer
from taskly.infrastructure.exceptions.smtp import SMTPServerTimeoutError


SEND_TIMEOUT: Final[int] = 5

class SmtpEmailSenderGateway(EmailSenderGateway):

    def __init__(
        self,
        render: TemplateRenderer,
        config: EmailConnectionConfig,
    ) -> None:
        self._render = render
        self._config = config

    async def send(self, to: str, subject: str, template_name: str, context: dict) -> None:
        html = self._render.render(template_name, context)

        message = MIMEMultipart("alternative")
        message["From"] = self._config.sender
        message["To"] = to
        message["Subject"] = subject

        message.attach(MIMEText(html, "html"))

        ssl_context = ssl.create_default_context()

        if self._config.use_ssl:
            ssl_context.check_hostname = self._config.use_ssl
            ssl_context.verify_mode = ssl.CERT_REQUIRED
        else:
            ssl_context.check_hostname = self._config.use_ssl
            ssl_context.verify_mode = ssl.CERT_NONE


        try:
            await aiosmtplib.send(
                message,
                username=self._config.username,
                timeout=SEND_TIMEOUT,
                hostname=self._config.hostname,
                port=self._config.port,
                start_tls=self._config.use_tls,
                tls_context=ssl_context,
                sender=self._config.sender,
                password=self._config.password,
            )
        except SMTPConnectTimeoutError as err:
            raise SMTPServerTimeoutError(orig_error=err)

