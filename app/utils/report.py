"""
This module is responsible for sending messages to admins
"""

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import AiogramError, TelegramAPIError

from marzban import NodeResponse

from utils import EnvSettings, MessageTexts, logger

bot = Bot(
    token=EnvSettings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def send_message(message: str):
    """
    Sends a message to all admins.
    """
    try:
        for admin_chatid in EnvSettings.TELEGRAM_ADMINS_ID:
            await bot.send_message(chat_id=admin_chatid, text=message)
    except (AiogramError, TelegramAPIError) as e:
        logger.error("Failed send report message: %s", str(e))


async def node_error(node: NodeResponse):
    """
    Sends a notification to admins about a node error.
    """
    text = (MessageTexts.NODE_ERROR).format(
        name=node.name, ip=node.address, message=node.message or "None"
    )
    await send_message(text)


async def node_restart(node: NodeResponse, success: bool):
    """
    Sends a notification to admins about the result of a node restart.
    """
    text = (
        (MessageTexts.NODE_AUTO_RESTART_DONE).format(name=node.name)
        if success is True
        else (MessageTexts.NODE_AUTO_RESTART_ERROR).format(name=node.name)
    )
    await send_message(text)
