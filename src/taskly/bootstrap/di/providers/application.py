from dishka import Scope, provide_all, Provider, provide

from taskly.application.common.gateway.email_verification_code_storage import EmailVerificationCodeStorage
from taskly.application.common.service.email_verification_code_generator import EmailVerificationCodeGenerator
from taskly.application.common.service.email_verification_code_url_generator import EmailVerificationCodeUrlGenerator
from taskly.infrastructure.auth.adapters.email_verification_code_storage_redis import RedisEmailVerificationCodeStorage


class ApplicationServices(Provider):
    scope = Scope.REQUEST

    services = provide_all(
        EmailVerificationCodeGenerator,
        EmailVerificationCodeUrlGenerator
    )


class ApplicationGateways(Provider):
    scope = Scope.REQUEST

    email_verification_code_storage = provide(RedisEmailVerificationCodeStorage, provides=EmailVerificationCodeStorage)

def application_providers() -> tuple[Provider, ...]:
    return (
        ApplicationServices(),
        ApplicationGateways()
    )
