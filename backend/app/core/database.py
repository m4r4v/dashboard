from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

class DatabaseSessionManager:
    def __init__(self):
        self._engine = None
        self._sessionmaker = None

    def init_db(self, db_url: str):
        connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}
        self._engine = create_async_engine(
            db_url, pool_pre_ping=True, connect_args=connect_args, echo=False
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine, expire_on_commit=False, autoflush=False, autocommit=False
        )

    async def close(self):
        if self._engine is not None:
            await self._engine.dispose()

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

sessionmanager = DatabaseSessionManager()

async def get_db_session():
    async with sessionmanager.session() as session:
        yield session