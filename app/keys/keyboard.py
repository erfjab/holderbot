from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db import Server
from app.keys.callback import Pages, Actions, PageCB
from app.settings import KeyboardText


class Keyboards:
    @classmethod
    def home(cls, servers: list[Server] = None) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        if servers:
            for server in servers:
                kb.button(
                    text=server.remark,
                    callback_data=PageCB(
                        page=Pages.SERVER, action=Actions.READ, server=server.id
                    ).pack(),
                )

        kb.adjust(1)
        kb.add(
            InlineKeyboardButton(
                text=KeyboardText.NEW_SERVER,
                callback_data=PageCB(page=Pages.SERVER, action=Actions.CREATE).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardText.UPDATE_DATA, callback_data=PageCB().pack()
            ),
        )
        return kb.as_markup()
