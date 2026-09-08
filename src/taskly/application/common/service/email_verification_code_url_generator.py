import random
import string
from typing import Tuple
from urllib.parse import urlunparse, urlencode

from taskly.bootstrap.configs.server_config import ServerConfig

class EmailVerificationCodeUrlGenerator:


    def __init__(self, server_config: ServerConfig) -> None:
        self._server_config = server_config

    async def generate(self, email: str) -> str:
        """
        First value is redirect url to submit verification code
        :return:
        """

        email_param = {"email": email}

        url = urlunparse((
            'https',
            self._server_config.client_domain,
            self._server_config.email_verification_code_url,
            '',
            urlencode(email_param),
            '',
        ))

        return url
