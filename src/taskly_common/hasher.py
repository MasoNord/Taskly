from hashlib import blake2b
from hmac import compare_digest
from typing import Final

from taskly.bootstrap.config_loader import Config

config = Config.load()
AUTH_SIZE: Final[int] = 16

def sign(value: bytes) -> bytes:
    h = blake2b(digest_size=AUTH_SIZE, key=config.server.hash_secrete.encode("utf-8"))
    h.update(value)
    return h.hexdigest().encode('utf-8')

def verify(cookie: bytes, sig: bytes) -> bool:
    good_sig = sign(cookie)
    return compare_digest(good_sig, sig)