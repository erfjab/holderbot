import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from jobs import stop_scheduler, start_scheduler
from middlewares.auth import CheckAdminAccess
from routers import setup_routers
from utils.config import TELEGRAM_BOT_TOKEN
from utils.log import logger
from utils.statedb import storage


async def on_startup() -> None:
    """Function to execute during bot startup."""
    logger.info("Bot is starting up...")

    logger.info("Starting scheduler...")

    run_job = await start_scheduler()  # Start scheduled tasks
    if not run_job:
        raise SystemExit(
            logger.critical("Stopping the bot due to scheduler startup failure.")
        )  # Stop the bot if scheduler fails
    logger.info("Scheduler is running.")
    logger.info("Bot is up and running!")


async def on_shutdown() -> None:
    """Function to execute during bot shutdown."""
    logger.info("Bot is shutting down...")
    logger.info("Stopping scheduler...")
    await stop_scheduler()  # Stop scheduled tasks
    logger.info("Scheduler has stopped.")
    logger.info("Bot has shut down successfully.")


async def main() -> None:
    """Function to run aiogram bot."""
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
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
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"An error occurred while polling: {e}")


if __name__ == "__main__":
    try:
        # Run the main function using asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Bot stopped by user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
