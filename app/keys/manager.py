from enum import Enum
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.settings.language import KeyboardTexts
from app.db import Server
from ._enums import Pages, Actions
from ._callbacks import PageCB, SelectCB


class _KeyboardsManager:
    def home(self, servers: list[Server] = []) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for server in servers:
            kb.button(
                text=server.remark,
                callback_data=PageCB(
                    page=Pages.MENU, action=Actions.LIST, panel=server.id
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

    def menu(self, panel: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        items = {KeyboardTexts.USERS: Pages.USERS}

        for text, page in items.items():
            kb.button(
                text=text,
                callback_data=PageCB(
                    page=page, action=Actions.LIST, panel=panel
                ).pack(),
            )

        kb.adjust(2)

        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.SERVER,
                callback_data=PageCB(
                    page=Pages.SERVERS, action=Actions.INFO, panel=panel
                ).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardTexts.HOMES,
                callback_data=PageCB(page=Pages.HOME).pack(),
            ),
            width=2,
        )

        return kb.as_markup()

    def lister(
        self, items: list[Server], page: Pages, panel: int
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for item in items:
            kb.button(
                text=f"{item.emoji if item.emoji else ''}{item.remark}",
                callback_data=PageCB(
                    page=page, action=Actions.INFO, dataid=item.id, panel=panel
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

    def selector(
        self,
        data: list[str],
        types: str,
        action: Actions | None = None,
        selects: list[str] | None = None,
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for d in data:
            text = d.value if isinstance(d, Enum) else d
            selected = False

            if selects is not None:
                selected = d in selects
                text = f"✅ {text}" if selected else f"❌ {text}"

            kb.button(
                text=text,
                callback_data=SelectCB(
                    select=d, types=types, action=action, selected=selected
                ).pack(),
            )

        kb.adjust(2)

        if selects is not None:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.DONE,
                    callback_data=SelectCB(
                        types=types, action=Actions.CREATE, done=True
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=KeyboardTexts.HOMES,
                    callback_data=PageCB(page=Pages.HOME).pack(),
                ),
                width=2,
            )

        else:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.HOMES,
                    callback_data=PageCB(page=Pages.HOME).pack(),
                ),
                width=1,
            )

        return kb.as_markup()

    def modify(
        self, dataid: int, datatypes: list[Enum], page: Pages, panel: int
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for datatype in datatypes:
            kb.button(
                text=datatype.value,
                callback_data=PageCB(
                    page=page,
                    action=Actions.MODIFY,
                    dataid=dataid,
                    datatype=datatype,
                    panel=panel,
                ).pack(),
            )

        kb.adjust(2)
        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.HOMES,
                callback_data=PageCB(page=Pages.HOME).pack(),
            ),
            width=1,
        )

        return kb.as_markup()
