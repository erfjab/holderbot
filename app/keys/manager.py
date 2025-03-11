from enum import Enum
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.settings.language import KeyboardTexts
from app.db import Server
from ._enums import Pages, Actions, SelectAll
from ._callbacks import PageCB, SelectCB


class _KeyboardsManager:
    def home(self, servers: list[Server] = []) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for server in servers:
            kb.button(
                text=f"{server.emoji if server.emoji else ''}{server.remark}",
                callback_data=PageCB(
                    page=Pages.MENU, action=Actions.LIST, panel=server.id
                ).pack(),
            )

        kb.adjust(2)

        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.TEMPLATES,
                callback_data=PageCB(page=Pages.TEMPLATES, action=Actions.LIST).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardTexts.UPDATE_CHECKER,
                callback_data=PageCB(page=Pages.UPDATE, action=Actions.INFO).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardTexts.CREATE_SERVER,
                callback_data=PageCB(page=Pages.SERVERS, action=Actions.CREATE).pack(),
            ),
            width=2,
        )

        return kb.as_markup()

    def menu(self, panel: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        items = {
            KeyboardTexts.USERS: Pages.USERS,
            KeyboardTexts.ACTIONS: Pages.ACTIONS,
            KeyboardTexts.STATS: Pages.STATS,
        }

        for text, page in items.items():
            kb.button(
                text=text,
                callback_data=PageCB(
                    page=page, action=Actions.LIST, panel=panel
                ).pack(),
            )
        kb.button(
            text=KeyboardTexts.CREATE_USER,
            callback_data=PageCB(
                page=Pages.USERS, action=Actions.CREATE, panel=panel
            ).pack(),
        )
        kb.button(
            text=KeyboardTexts.SEARCH_USER,
            callback_data=PageCB(
                page=Pages.USERS, action=Actions.SEARCH, panel=panel
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
        self,
        items: list[Server],
        page: Pages,
        panel: int | None = None,
        control: tuple[int, int] = None,
        filters: list[str] | None = None,
        select_filters: str | None = None,
        search: bool = False,
        server_back: int | None = None,
        user_back: int | None = None,
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for item in items:
            kb.button(
                text=f"{item.emoji if item.emoji else ''}{item.remark}",
                callback_data=PageCB(
                    page=page,
                    action=Actions.INFO,
                    dataid=item.id,
                    panel=panel,
                    filters=select_filters,
                ).pack(),
            )

        kb.adjust(2)

        buttons = []
        if filters is not None:
            for f in filters:
                buttons.append(
                    InlineKeyboardButton(
                        text=f,
                        callback_data=PageCB(
                            page=page,
                            action=Actions.LIST,
                            panel=panel,
                            filters=f,
                        ).pack(),
                    )
                )
            if buttons:
                kb.row(*buttons, width=len(filters))

        if control is not None:
            left, right = control
            buttons = []
            if left != 0:
                buttons.append(
                    InlineKeyboardButton(
                        text=KeyboardTexts.LEFT,
                        callback_data=PageCB(
                            page=page,
                            action=Actions.LIST,
                            pagenumber=left,
                            panel=panel,
                            filters=select_filters,
                        ).pack(),
                    )
                )
            if right != 0:
                buttons.append(
                    InlineKeyboardButton(
                        text=KeyboardTexts.RIGHT,
                        callback_data=PageCB(
                            page=page,
                            action=Actions.LIST,
                            pagenumber=right,
                            panel=panel,
                            filters=select_filters,
                        ).pack(),
                    )
                )
            if buttons:
                kb.row(*buttons, width=2)
        if search:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.SEARCH_USER,
                    callback_data=PageCB(
                        page=Pages.USERS, action=Actions.SEARCH, panel=panel
                    ).pack(),
                ),
                width=1,
            )
        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.CREATE,
                callback_data=PageCB(
                    page=page, action=Actions.CREATE, panel=panel
                ).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardTexts.HOMES,
                callback_data=PageCB(page=Pages.HOME).pack(),
            ),
            width=2,
        )
        if server_back and not user_back:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.BACK,
                    callback_data=PageCB(
                        page=Pages.MENU, action=Actions.LIST, panel=server_back
                    ).pack(),
                ),
                width=1,
            )
        if server_back and user_back:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.BACK,
                    callback_data=PageCB(
                        page=Pages.USERS,
                        action=Actions.INFO,
                        dataid=user_back,
                        panel=server_back,
                    ).pack(),
                ),
                width=1,
            )
        return kb.as_markup()

    def cancel(
        self,
        server_back: int | None = None,
        user_back: int | None = None,
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        kb.button(
            text=KeyboardTexts.HOMES, callback_data=PageCB(page=Pages.HOME).pack()
        )

        if server_back and not user_back:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.BACK,
                    callback_data=PageCB(
                        page=Pages.MENU, action=Actions.LIST, panel=server_back
                    ).pack(),
                ),
                width=1,
            )
        if server_back and user_back:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.BACK,
                    callback_data=PageCB(
                        page=Pages.USERS,
                        action=Actions.INFO,
                        dataid=user_back,
                        panel=server_back,
                    ).pack(),
                ),
                width=1,
            )

        return kb.as_markup()

    def selector(
        self,
        data: list[str | tuple[str, str]],
        types: str,
        action: Actions | None = None,
        selects: list[str] | None = None,
        width: int = 2,
        panel: int | None = None,
        extra: str | None = None,
        all_selects: bool = False,
        user_back: int | None = None,
        server_back: int | None = None,
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for d in data:
            text = d.value if isinstance(d, Enum) else d
            if isinstance(d, tuple):
                display_name, value = d
            else:
                display_name = value = d.value if isinstance(d, Enum) else d
            selected = False

            if selects is not None:
                selected = value in selects
                display_name = f"✅ {text}" if selected else f"❌ {text}"

            kb.button(
                text=display_name,
                callback_data=SelectCB(
                    select=value,
                    types=types,
                    action=action,
                    selected=selected,
                    panel=panel,
                    extra=extra,
                ).pack(),
            )

        kb.adjust(width)

        if all_selects:
            select_buttons = []
            if len(selects) != len(data) and len(selects) > 0:
                select_buttons.extend(
                    [
                        InlineKeyboardButton(
                            text=KeyboardTexts.SELECTS_ALL,
                            callback_data=SelectCB(
                                types=types,
                                action=action,
                                panel=panel,
                                extra=extra,
                                select=SelectAll.SELECT,
                            ).pack(),
                        ),
                        InlineKeyboardButton(
                            text=KeyboardTexts.DESELECTS_ALL,
                            callback_data=SelectCB(
                                types=types,
                                action=action,
                                panel=panel,
                                extra=extra,
                                select=SelectAll.DESELECT,
                            ).pack(),
                        ),
                    ]
                )
            elif len(selects) == len(data):
                select_buttons.append(
                    InlineKeyboardButton(
                        text=KeyboardTexts.DESELECTS_ALL,
                        callback_data=SelectCB(
                            types=types,
                            action=action,
                            panel=panel,
                            extra=extra,
                            select=SelectAll.DESELECT,
                        ).pack(),
                    )
                )
            elif len(selects) == 0:
                select_buttons.append(
                    InlineKeyboardButton(
                        text=KeyboardTexts.SELECTS_ALL,
                        callback_data=SelectCB(
                            types=types,
                            action=action,
                            panel=panel,
                            extra=extra,
                            select=SelectAll.SELECT,
                        ).pack(),
                    )
                )

            if select_buttons:
                kb.row(*select_buttons, width=len(select_buttons))

        if selects is not None:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.DONE,
                    callback_data=SelectCB(
                        types=types,
                        action=action,
                        done=True,
                        panel=panel,
                        extra=extra,
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

        if server_back and not user_back:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.BACK,
                    callback_data=PageCB(
                        page=Pages.MENU, action=Actions.LIST, panel=server_back
                    ).pack(),
                ),
                width=1,
            )
        if server_back and user_back:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.BACK,
                    callback_data=PageCB(
                        page=Pages.USERS,
                        action=Actions.INFO,
                        dataid=user_back,
                        panel=server_back,
                    ).pack(),
                ),
                width=1,
            )

        return kb.as_markup()

    def modify(
        self,
        dataid: int,
        datatypes: list[Enum],
        page: Pages,
        panel: int | None = None,
        server_back: int | None = None,
        user_back: int | None = None,
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

        if server_back and not user_back:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.BACK,
                    callback_data=PageCB(
                        page=Pages.MENU, action=Actions.LIST, panel=server_back
                    ).pack(),
                ),
                width=1,
            )
        if server_back and user_back:
            kb.row(
                InlineKeyboardButton(
                    text=KeyboardTexts.BACK,
                    callback_data=PageCB(
                        page=Pages.USERS,
                        action=Actions.INFO,
                        dataid=user_back,
                        panel=server_back,
                    ).pack(),
                ),
                width=1,
            )

        return kb.as_markup()
