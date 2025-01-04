from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.settings.language import KeyboardTexts
from app.db import Server
from ._enums import Pages, Actions
from ._callbacks import PageCB


class _KeyboardsManager:
    def home(self, servers: list[Server] = []) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for server in servers:
            kb.button(
                text=server.remark,
                callback_data=PageCB(
                    page=Pages.MENU, action=Actions.INFO, panel=server.id
                ).pack(),
            )

        kb.adjust(2)

        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.CREATE,
                callback_data=PageCB(page=Pages.SERVERS, action=Actions.CREATE).pack(),
            ),
            width=1,
        )

        return kb.as_markup()

    def lister(
        self,
        items: list[Server],
        page: Pages,
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for item in items:
            kb.button(
                text=item.remark,
                callback_data=PageCB(
                    page=page, action=Actions.INFO, dataid=item.id
                ).pack(),
            )

        kb.adjust(2)

        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.CREATE,
                callback_data=PageCB(page=page, action=Actions.CREATE).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardTexts.HOMES,
                callback_data=PageCB(page=Pages.HOME).pack(),
            ),
            width=2,
        )

        return kb.as_markup()

    def cancel(
        self,
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        kb.button(
            text=KeyboardTexts.HOMES, callback_data=PageCB(page=Pages.HOME).pack()
        )
        return kb.as_markup()
