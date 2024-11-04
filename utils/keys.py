from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from marzban import ProxyInbound, Admin, UserResponse

from utils.lang import KeyboardTexts
from models import (
    PagesActions,
    PagesCallbacks,
    AdminActions,
    AdminSelectCallbacks,
    UserStatusCallbacks,
    UserInboundsCallbacks,
    ConfirmCallbacks,
    BotActions,
)


class BotKeyboards:

    @staticmethod
    def home() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.button(
            text=KeyboardTexts.UserCreate,
            callback_data=PagesCallbacks(page=PagesActions.UserCreate).pack(),
        )
        kb.button(
            text=KeyboardTexts.NodeMonitoring,
            callback_data=PagesCallbacks(page=PagesActions.NodeMonitoring).pack(),
        )
        kb.button(
            text=KeyboardTexts.UsersMenu,
            callback_data=PagesCallbacks(page=PagesActions.UsersMenu).pack(),
        )
        return kb.adjust(2).as_markup()

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
        just_one_inbound: bool = False,
    ):
        kb = InlineKeyboardBuilder()
        for protocol_list in inbounds.values():
            for inbound in protocol_list:
                is_selected = inbound["tag"] in selected
                kb.button(
                    text=f"{('✅' if is_selected else '❌') if not just_one_inbound else '🔘'} {inbound['tag']} ({inbound['protocol']})",
                    callback_data=UserInboundsCallbacks(
                        tag=inbound["tag"],
                        protocol=inbound["protocol"],
                        is_selected=is_selected,
                        action=action,
                        just_one_inbound=just_one_inbound,
                        is_done=just_one_inbound,
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

    @staticmethod
    def node_monitoring() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        kb.button(
            text=KeyboardTexts.NodeMonitoringChecker,
            callback_data=ConfirmCallbacks(
                page=BotActions.NodeChecker, action=AdminActions.Edit, is_confirm=True
            ),
        )
        kb.button(
            text=KeyboardTexts.NodeMonitoringAutoRestart,
            callback_data=ConfirmCallbacks(
                page=BotActions.NodeAutoRestart,
                action=AdminActions.Edit,
                is_confirm=True,
            ),
        )
        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.Home,
                callback_data=PagesCallbacks(page=PagesActions.Home).pack(),
            ),
        )
        return kb.adjust(2).as_markup()

    @staticmethod
    def users() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        kb.button(
            text=KeyboardTexts.UsersAddInbound,
            callback_data=ConfirmCallbacks(
                page=BotActions.UsersInbound, action=AdminActions.Add
            ),
        )
        kb.button(
            text=KeyboardTexts.UsersDeleteInbound,
            callback_data=ConfirmCallbacks(
                page=BotActions.UsersInbound, action=AdminActions.Delete
            ),
        )
        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.Home,
                callback_data=PagesCallbacks(page=PagesActions.Home).pack(),
            ),
        )
        return kb.adjust(2).as_markup()

    @staticmethod
    def user(user: UserResponse) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        kb.button(
            text=KeyboardTexts.UserCreateLinkCopy,
            copy_text=CopyTextButton(text=user.subscription_url)
        )
        return kb.as_markup()