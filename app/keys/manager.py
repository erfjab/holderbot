from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.settings.language import KeyboardTexts
from ._enums import Pages
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
