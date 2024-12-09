import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.settings import EnvFile, logger
from app.routers import setup_routers
from app.settings.middlewares import CheckUserAccess


async def main() -> None:
    """Initialize and run the bot."""
    bot = Bot(
        token=EnvFile.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML, link_preview_is_disabled=True
        ),
    )
    dp = Dispatcher()
    dp.update.middleware(CheckUserAccess())
    dp.include_router(router=setup_routers())
    try:
        bot_info = await bot.get_me()
        await bot.delete_webhook(True)
        logger.info("Polling messages for @%s", bot_info.username)
        await dp.start_polling(bot)
    except (ConnectionError, TimeoutError, asyncio.TimeoutError) as conn_err:
        logger.error("Polling error (connection issue): %s", conn_err)
    except RuntimeError as runtime_err:
        logger.error("Runtime error during polling: %s", runtime_err)
    except asyncio.CancelledError:
        logger.warning("Polling was cancelled.")
