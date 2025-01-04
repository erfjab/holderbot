import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Base
from .config import engine, async_session


class DatabaseManager:
    def __init__(self):
        self._connection_lock = asyncio.Lock()
        self._is_initialized = False

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self._is_initialized:
            await self.init()

        async with self._connection_lock:
            async with async_session() as session:
                async with session.begin():
                    yield session

    async def init(self) -> None:
        """Initialize the database by creating all tables if they don't exist."""
        if not self._is_initialized:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            self._is_initialized = True
