from typing import AsyncIterator

import structlog
from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine

from taskly.bootstrap.configs.database_config import LocalDBConnectionConfig, EngineSettings

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

def infrastructure_providers() -> tuple[Provider, ...]:
    return (
        LocalDatabaseProvider(),
    )
