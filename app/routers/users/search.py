from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.keys import BotKeys, Pages
from app.db import crud
from app.settings.language import MessageTexts
from app.api import ClinetManager
from app.settings.track import tracker

router = Router(name="users_search")


@router.message(Command(commands=["user"]))
async def data(message: Message):
    try:
        _, serverid, username = message.text.split(maxsplit=2)
    except ValueError:
        track = await message.reply(
            text=f"{MessageTexts.WRONG_PATTERN}\n/user serverid username",
            reply_markup=BotKeys.cancel(),
        )
        return await tracker.add(track)

    server = await crud.get_server(int(serverid))
    if not server:
        track = await message.reply(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    users = await ClinetManager.get_users(server, page=1, size=10, search=username)

    track = await message.answer(
        text=MessageTexts.ITEMS,
        reply_markup=BotKeys.lister(
            items=users,
            page=Pages.USERS,
            panel=server.id,
        ),
    )
    return await tracker.cleardelete(message, track)
