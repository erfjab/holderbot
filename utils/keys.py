from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from marzban import ProxyInbound, Admin

from utils.lang import KeyboardTexts
from models import (
    PagesActions,
    PagesCallbacks,
    AdminActions,
    AdminSelectCallbacks,
    UserStatusCallbacks,
    UserInboundsCallbacks,
)


class BotKeyboards:

    @staticmethod
    def home() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.button(
            text=KeyboardTexts.UserCreate,
            callback_data=PagesCallbacks(page=PagesActions.UserCreate).pack(),
        )
        return kb.as_markup()

    @staticmethod
    def cancel() -> InlineKeyboardMarkup:
        return (
            InlineKeyboardBuilder()
            .row(
                InlineKeyboardButton(
                    text=KeyboardTexts.Home,
                    callback_data=PagesCallbacks(page=PagesActions.Home).pack(),
                )
            )
            .as_markup()
        )

    @staticmethod
    def user_status(action: AdminActions) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.Active,
                callback_data=UserStatusCallbacks(
                    status="active", action=action
                ).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardTexts.OnHold,
                callback_data=UserStatusCallbacks(
                    status="on_hold", action=action
                ).pack(),
            ),
        )
        kb.button(
            text=KeyboardTexts.Home,
            callback_data=PagesCallbacks(page=PagesActions.Home).pack(),
        )
        return kb.adjust(2).as_markup()

    @staticmethod
    def inbounds(
        inbounds: dict[str, list[ProxyInbound]],
        selected: set[str] = [],
        action: AdminActions = AdminActions.Add,
    ):
        kb = InlineKeyboardBuilder()
        for protocol_list in inbounds.values():
            for inbound in protocol_list:
                is_selected = inbound["tag"] in selected
                kb.button(
                    text=f"{'✅' if is_selected else '❌'} {inbound['tag']} ({inbound['protocol']})",
                    callback_data=UserInboundsCallbacks(
                        tag=inbound["tag"],
                        protocol=inbound["protocol"],
                        is_selected=is_selected,
                        action=action,
                    ),
                )
        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.Finish,
                callback_data=UserInboundsCallbacks(action=action, is_done=True).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardTexts.Home,
                callback_data=PagesCallbacks(page=PagesActions.Home).pack(),
            ),
        )
        return kb.adjust(2).as_markup()

    @staticmethod
    def admins(admins: list[Admin]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for admin in admins:
            kb.button(
                text=admin.username,
                callback_data=AdminSelectCallbacks(username=admin.username),
            )

        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.Home,
                callback_data=PagesCallbacks(page=PagesActions.Home).pack(),
            ),
        )
        return kb.adjust(2).as_markup()
