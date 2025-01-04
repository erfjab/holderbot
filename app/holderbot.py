import asyncio

from aiogram import Dispatcher

from app.settings.log import logger
from app.routers import setup_routers
from app.settings.tasks import tasker
from .bot import bot


async def main() -> None:
    """Initialize and run the bot."""
    dp = Dispatcher()
    dp.include_router(router=setup_routers())

    try:
        await tasker.start()
        await bot.delete_webhook(True)
        logger.info("Start Polling messages")
        await dp.start_polling(bot)
    except (ConnectionError, TimeoutError, asyncio.TimeoutError) as conn_err:
        logger.error("Polling error (connection issue): %s", conn_err)
    except RuntimeError as runtime_err:
        logger.error("Runtime error during polling: %s", runtime_err)
    except asyncio.CancelledError:
        logger.warning("Polling was cancelled.")
