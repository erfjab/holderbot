from typing import Optional
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from app.settings.config import env


class BotInstall:
    _instance: Optional[Bot] = None

    @classmethod
    def bot(cls) -> Bot:
        """Get or create bot instance"""
        if cls._instance is None:
            cls._instance = Bot(
                token=env.TELEGRAM_BOT_TOKEN,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML, link_preview_is_disabled=True
                ),
            )
        return cls._instance


bot = BotInstall().bot()
