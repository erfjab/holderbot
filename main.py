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
from utils import EnvSettings, logger, Storage


async def on_startup() -> None:
    """Execute startup tasks for HolderBot."""
    logger.info("Starting HolderBot...")

    admin_ids = ", ".join(map(str, EnvSettings.TELEGRAM_ADMINS_ID))
    logger.debug(f"Admin IDs: {admin_ids}")  # Admin IDs only logged for debug

    # Start the scheduler
    if not await start_scheduler():
        logger.critical("Scheduler startup failed. Shutting down.")
        raise SystemExit

    logger.info("Scheduler started successfully. Bot is now running.")


async def on_shutdown() -> None:
    """Execute shutdown tasks for HolderBot."""
    logger.info("Shutting down HolderBot...")
    await stop_scheduler()
    logger.info("Scheduler stopped. Shutdown complete.")


async def main() -> None:
    """Initialize and run the bot."""
    bot = Bot(
        token=EnvSettings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML, link_preview_is_disabled=True
        ),
    )
    dp = Dispatcher(storage=Storage)

    # Setup dispatcher with routers and middleware
    dp.include_router(setup_routers())
    dp.update.middleware(CheckAdminAccess())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Start polling for bot messages
    try:
        bot_info = await bot.get_me()
        logger.info(f"Polling messages for HolderBot [@{bot_info.username}]...")
        await dp.start_polling(bot)
    except (ConnectionError, TimeoutError) as conn_err:
        logger.error(f"Polling error (connection issue): {conn_err}")
    except Exception as e:  # Capture unexpected errors
        logger.error(f"Unexpected error during polling: {e}")


if __name__ == "__main__":
    try:
        logger.info("Launching HolderBot...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Bot stopped manually by user.")
    except Exception as e:
        logger.error(f"Unexpected fatal error: {e}")
