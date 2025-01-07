import asyncio

from aiogram import Dispatcher

from app.settings.log import logger
from app.settings.tasks import tasker
from app.settings.track import tracker
from app.routers import setup_routers
from app.settings.middlewares import CheckUserAccess
from .bot import bot
from .version import __version__


async def main() -> None:
    """Initialize and run the bot."""
    try:
        dp = Dispatcher(storage=tracker)
        dp.include_router(router=setup_routers())
        dp.update.middleware(CheckUserAccess())
        await tasker.start()
        await bot.delete_webhook(True)
        logger.info(f"Start Polling {__version__}")
        await dp.start_polling(bot)
    except (ConnectionError, TimeoutError, asyncio.TimeoutError) as conn_err:
        logger.error("Polling error (connection issue): %s", conn_err)
    except RuntimeError as runtime_err:
        logger.error("Runtime error during polling: %s", runtime_err)
    except asyncio.CancelledError:
        logger.warning("Polling was cancelled.")
