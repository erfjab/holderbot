from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from marzban import NodeResponse

from utils.lang import MessageTexts
from utils.config import TELEGRAM_BOT_TOKEN, TELEGRAM_ADMINS_ID

bot = Bot(
    token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


async def send_message(message: str):
    try:
        for admin_chatid in TELEGRAM_ADMINS_ID:
            await bot.send_message(chat_id=admin_chatid, text=message)
    except:
        pass


async def node_error(node: NodeResponse):
    text = (MessageTexts.NodeError).format(
        name=node.name, ip=node.address, message=node.message or "None"
    )
    await send_message(text)


async def node_restart(node: NodeResponse, success: bool):
    text = (
        (MessageTexts.NodeAutoRestartDone).format(name=node.name)
        if success is True
        else (MessageTexts.NodeAutoRestartError).format(name=node.name)
    )
    await send_message(text)
