from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.settings.language import KeyboardTexts
from app.db import Server
from ._enums import Pages, Actions
from ._callbacks import PageCB


class _KeyboardsManager:
    def home(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        keys = {
            KeyboardTexts.SERVERS: Pages.SERVERS,
        }
        for text, page in keys.items():
            kb.button(text=text, callback_data=PageCB(page=page).pack())

        return kb.adjust(2).as_markup()

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
