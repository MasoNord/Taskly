from typing import AsyncIterator

import redis
import structlog
from dishka import Provider, provide, Scope, provide_all
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine

from taskly.application.common.gateway.email_sender import EmailSenderGateway
from taskly.bootstrap.configs.database_config import LocalDBConnectionConfig, EngineSettings
from taskly.bootstrap.configs.email_config import EmailTemplateRendererConfig
from taskly.bootstrap.configs.redis_config import RedisConfig
import redis.asyncio as aioredis

from taskly.infrastructure.auth.handlers.sign_up_via_email import GetEmailVerificationCodeUrl
from taskly.infrastructure.email.gateway.email_sender_smtp import SmtpEmailSenderGateway
from taskly.infrastructure.email.template_renderer import TemplateRenderer
from taskly.infrastructure.exceptions.redis import RedisConnectionError

logger = structlog.get_logger(__name__)


class LocalDatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_async_engine(
        self,
        postgres: LocalDBConnectionConfig,
        engine_settings: EngineSettings,
    ) -> AsyncIterator[AsyncEngine]:
        async_engine = create_async_engine(
            url=postgres.postgres_conn_url,
            echo=engine_settings.echo,
            echo_pool=engine_settings.echo_pool,
            pool_size=engine_settings.pool_size,
            max_overflow=engine_settings.max_overflow,
            connect_args={"timeout": 5},
            pool_pre_ping=True,
        )

        logger.debug("Local async engine created with DSN %s", postgres.postgres_conn_url)
        yield async_engine
        logger.debug("Disposing async engine...")
        await async_engine.dispose()
        logger.debug("Engine is disposed")

    @provide(scope=Scope.APP)
    def provide_async_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        async_session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )
        logger.debug("Async session maker initialized")
        return async_session_factory

    @provide(scope=Scope.REQUEST)
    async def provide_main_async_session(
        self,
        async_session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:

        logger.debug("Starting Main async session...")
        async with async_session_factory() as session:
            logger.debug("Main async session started.")
            yield session
            logger.debug("Closing Main async session.")
        logger.debug("Main async session closed.")


class LocalRedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_async_redis_pool(self, redis_config: RedisConfig) -> AsyncIterator[aioredis.ConnectionPool]:

        pool = aioredis.ConnectionPool.from_url(
            redis_config.redis_conn_url,
            max_connections=redis_config.max_connections,
            decode_responses=redis_config.decode_response,
        )

        logger.debug("Local async redis pool started...")
        yield pool
        logger.debug("Local async redis pool closing...")
        await pool.disconnect()
        logger.debug("Local async redis pool is closed!")

    @provide(scope=Scope.REQUEST)
    async def provide_async_redis_connection(self, local_redis_pool: aioredis.ConnectionPool) -> AsyncIterator[aioredis.Connection]:
        logger.debug("Starting Local redis connection...")
        redis_client = aioredis.Redis(connection_pool=local_redis_pool)

        try:
            await redis_client.ping()
        except redis.exceptions.ConnectionError as err:
            logger.exception("Redis startup check failed: %s", err)
            raise RedisConnectionError from err

        yield redis_client
        logger.debug("Closing local redis connection...")
        await redis_client.close()
        logger.debug("Local redis connection is closed...")

class SmtpEmailSenderProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    def provide_renderer_environment(self, config: EmailTemplateRendererConfig) -> Environment:
        return Environment(loader=FileSystemLoader(config.template_path_folder))

    template_renderer = provide(TemplateRenderer)

    smtp_email_sender_gateway = provide(SmtpEmailSenderGateway, provides=EmailSenderGateway)


class AuthProvider(Provider):
    pass

class AuthHandlersProvider(Provider):
    scope = Scope.REQUEST

    handlers = provide_all(
        GetEmailVerificationCodeUrl
    )


def infrastructure_providers() -> tuple[Provider, ...]:
    return (
        LocalDatabaseProvider(),
        AuthProvider(),
        AuthHandlersProvider(),
        SmtpEmailSenderProvider()
    )
