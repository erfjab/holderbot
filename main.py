"""
Main module for the Telegram bot application.
This module initializes and runs the bot with all necessary configurations,
including scheduler setup, router configuration, and middleware integration.
"""

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from jobs import stop_scheduler, start_scheduler
from middlewares.auth import CheckAdminAccess
from routers import setup_routers
from utils import EnvSettings, logger, storage


async def on_startup() -> None:
    """Function to execute during bot startup."""
    logger.info("HolderBot is starting up...")

    logger.info(
        "Admin IDs: %s", ", ".join(map(str, EnvSettings.TELEGRAM_ADMINS_ID))
    )  # Log admin IDs
    logger.info("Starting scheduler for HolderBot...")

    run_job = await start_scheduler()  # Start scheduled tasks
    if not run_job:
        raise SystemExit(
            logger.critical("Stopping HolderBot due to scheduler startup failure.")
        )  # Stop the bot if scheduler fails
    logger.info("Scheduler is running for HolderBot.")
    logger.info("HolderBot is up and running!")


async def on_shutdown() -> None:
    """Function to execute during bot shutdown."""
    logger.info("HolderBot is shutting down...")
    logger.info("Stopping scheduler...")
    await stop_scheduler()  # Stop scheduled tasks
    logger.info("Scheduler has stopped.")
    logger.info("HolderBot has shut down successfully.")


async def main() -> None:
    """Function to run aiogram bot."""
    bot = Bot(
        token=EnvSettings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML, link_preview_is_disabled=True
        ),
    )

    # Set up Dispatcher
    dp = Dispatcher(storage=storage)

    # Set routers to dp
    dp.include_router(setup_routers())

    # Set middleware for access control
    dp.update.middleware(CheckAdminAccess())

    # Register startup and shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Start polling the bot
    try:
        bot_info = await bot.get_me()
        logger.info("HolderBot [@%s] is starting to poll messages...", bot_info.username)
        await dp.start_polling(bot)
    except (ConnectionError, TimeoutError) as conn_err:
        logger.error("A connection error occurred while polling: %s", conn_err)
    except Exception as e:  # pylint: disable=broad-except
        logger.error("An error occurred while polling HolderBot: %s", e)


if __name__ == "__main__":
    try:
        # Run the main function using asyncio
        logger.info("Running HolderBot...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("HolderBot stopped by user.")
    except Exception as e:  # pylint: disable=broad-except
        logger.error("An unexpected error occurred in HolderBot: %s", e)
