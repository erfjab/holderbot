"""
Database base module.

This module provides the asynchronous engine, session factory, and base class for
declarative models.
"""

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


class Base(DeclarativeBase, AsyncAttrs):
    """Base class for declarative models using SQLAlchemy."""

    def save(self, session: AsyncSession) -> None:
        """Save the current instance to the database."""
        session.add(self)

    def delete(self, session: AsyncSession) -> None:
        """Delete the current instance from the database."""
        session.delete(self)


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session to the application.
    """
    async with AsyncSessionLocal() as session:
        yield session
