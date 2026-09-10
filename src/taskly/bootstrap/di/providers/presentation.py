import structlog
from dishka import Provider, Scope, from_context, provide
from starlette.requests import Request

from taskly.bootstrap.configs.auth_config import CookiesConfig
from taskly.presentation.auth.cookie_params import CookieParams

logger = structlog.getLogger(__name__)

class AuthPresentationProvider(Provider):
    scope = Scope.REQUEST

    request = from_context(provides=Request)

    @provide
    def provide_cookie_params(self, cookie_config: CookiesConfig) -> CookieParams:
        logger.debug("Set up CookieParams: secure: %s samesite: %s", cookie_config.secure, cookie_config.samesite)
        return CookieParams(secure=cookie_config.secure, samesite=cookie_config.samesite)


def presentation_providers() -> tuple[Provider, ...]:
    return (
        AuthPresentationProvider(),
    )