import random
import string
from typing import Final

VERIFICATION_CODE_LENGTH: Final[int] = 8


class EmailVerificationCodeGenerator:
    async def generate_verification_code(self) -> str:
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in
                       range(VERIFICATION_CODE_LENGTH))
