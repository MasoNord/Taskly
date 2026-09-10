from dishka import Scope, provide_all, Provider, provide

from taskly.application.common.gateway.email_verification_code_storage import EmailVerificationCodeStorage
from taskly.application.common.gateway.uow import UoW
from taskly.application.common.gateway.user import UserGateway
from taskly.application.common.service.email_verification_code_generator import EmailVerificationCodeGenerator
from taskly.application.common.service.email_verification_code_url_generator import EmailVerificationCodeUrlGenerator
from taskly.infrastructure.auth.adapters.email_verification_code_storage_redis import RedisEmailVerificationCodeStorage
from taskly.infrastructure.postgresql.gateway.uow import BaseSQLAlchemyUoW
from taskly.infrastructure.postgresql.gateway.user import SAUserGateway


class ApplicationServices(Provider):
    scope = Scope.REQUEST

    services = provide_all(
        EmailVerificationCodeGenerator,
        EmailVerificationCodeUrlGenerator
    )

class ApplicationGateways(Provider):
    scope = Scope.REQUEST

    email_verification_code_storage = provide(RedisEmailVerificationCodeStorage, provides=EmailVerificationCodeStorage)
    user_gateway = provide(SAUserGateway, provides=UserGateway)
    uow = provide(BaseSQLAlchemyUoW, provides=UoW)

def application_providers() -> tuple[Provider, ...]:
    return (
        ApplicationServices(),
        ApplicationGateways()
    )
