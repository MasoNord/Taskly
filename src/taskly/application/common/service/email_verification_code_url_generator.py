import random
import string
from typing import Tuple
from urllib.parse import urlunparse, urlencode

from taskly.bootstrap.configs.server_config import ServerConfig

class EmailVerificationCodeUrlGenerator:


    def __init__(self, server_config: ServerConfig) -> None:
        self._server_config = server_config

    async def generate(self) -> Tuple[str, str | None]:
        """
        First value is redirect url to submit verification code
        Second value is temp code which will be set as an identifier in storage
        :return:
        """
        temp_code = self._generate_temp_code()

        query_params = {
            'temp-code': temp_code,
        }

        url = urlunparse((
            'https',
            self._server_config.client_domain,
            self._server_config.email_verification_code_url,
            '',
            urlencode(query_params),
            '',
        ))

        return url, temp_code

    def _generate_temp_code(self, n: int = 16) -> str:
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
