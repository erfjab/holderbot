import os
import asyncio
from alembic import context
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from app.db.base import Base

config = context.config

if os.getenv("TESTING"):
    config.set_main_option("sqlalchemy.url", "sqlite+aiosqlite:///:memory:")
else:
    config.set_main_option("sqlalchemy.url", "sqlite+aiosqlite:///data/db.sqlite3")

# Set up loggers from config file if available
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata object for 'autogenerate' support in migrations
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(  # pylint: disable=no-member
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():  # pylint: disable=no-member
        context.run_migrations()  # pylint: disable=no-member


def do_run_migrations(connection: Connection) -> None:
    """
    Configures the context for a migration and executes the migrations.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,  # pylint: disable=no-member
    )

    with context.begin_transaction():  # pylint: disable=no-member
        context.run_migrations()  # pylint: disable=no-member


async def run_async_migrations() -> None:
    """
    Creates an asynchronous Engine and associates a connection
    with the Alembic migration context.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode using asynchronous connections.
    """
    asyncio.run(run_async_migrations())


# Run migrations based on the mode (offline or online)
if context.is_offline_mode():  # pylint: disable=no-member
    run_migrations_offline()
else:
    run_migrations_online()
