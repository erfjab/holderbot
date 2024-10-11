from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Create an asynchronous engine
engine = create_async_engine(
    "sqlite+aiosqlite:///data/db.sqlite3",
    connect_args={"check_same_thread": False},
    echo=False,
)

# Create an asynchronous session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)


# Define a base class for declarative models
class Base(DeclarativeBase, AsyncAttrs):
    pass


@asynccontextmanager
async def GetDB() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session to the application.
    """
    async with AsyncSessionLocal() as session:
        yield session
