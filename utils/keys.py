"""
Module for managing key configurations and callback handling for the bot.

This module defines functions to build and handle callback buttons, as well as
handling key actions related to users, nodes, and admins in the bot system.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from marzban import ProxyInbound, Admin, UserResponse
from utils.lang import KeyboardTextsFile
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

KeyboardTexts = KeyboardTextsFile()


class BotKeyboards:
    """
    A class containing static methods to generate various inline keyboards used by the bot.
    These keyboards are used for actions like creating users, monitoring nodes, managing users, etc.
    """

    @staticmethod
    def home() -> InlineKeyboardMarkup:
        """
        Generates the home screen keyboard with buttons for User creation,
        Node Monitoring, and Users Menu.
        """
        kb = InlineKeyboardBuilder()
        kb.button(
            text=KeyboardTexts.USER_CREATE,
            callback_data=PagesCallbacks(page=PagesActions.USER_CREATE).pack(),
        )
        kb.button(
            text=KeyboardTexts.NODE_MONITORING,
            callback_data=PagesCallbacks(page=PagesActions.NODE_MONITORING).pack(),
        )
        kb.button(
            text=KeyboardTexts.USERS_MENU,
            callback_data=PagesCallbacks(page=PagesActions.USERS_MENU).pack(),
        )
        return kb.adjust(2).as_markup()

    @staticmethod
    def cancel() -> InlineKeyboardMarkup:
        """
        Generates a cancel button to return to the home screen.
        """
        return (
            InlineKeyboardBuilder()
            .row(
                InlineKeyboardButton(
                    text=KeyboardTexts.HOME,
                    callback_data=PagesCallbacks(page=PagesActions.HOME).pack(),
                )
            )
            .as_markup()
        )

    @staticmethod
    def user_status(action: AdminActions) -> InlineKeyboardMarkup:
        """
        Generates a keyboard for changing user status to either 'active' or 'on hold'.
        """
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.ACTIVE,
                callback_data=UserStatusCallbacks(
                    status="active", action=action
                ).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardTexts.ON_HOLD,
                callback_data=UserStatusCallbacks(
                    status="on_hold", action=action
                ).pack(),
            ),
        )
        kb.button(
            text=KeyboardTexts.HOME,
            callback_data=PagesCallbacks(page=PagesActions.HOME).pack(),
        )
        return kb.adjust(2).as_markup()

    @staticmethod
    def inbounds(
        inbounds: dict[str, list[ProxyInbound]],
        selected: set[str] = None,
        action: AdminActions = AdminActions.ADD,
        just_one_inbound: bool = False,
    ) -> InlineKeyboardMarkup:
        """
        Generates a keyboard with available inbounds, allowing the user to select or deselect them.
        """
        if selected is None:
            selected = set()

        kb = InlineKeyboardBuilder()
        for protocol_list in inbounds.values():
            for inbound in protocol_list:
                is_selected = inbound["tag"] in selected
                kb.button(
                    text=f"{('✅' if is_selected else '❌') if not just_one_inbound else '🔘'} "
                    f"{inbound['tag']} ({inbound['protocol']})",
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
                text=KeyboardTexts.FINISH,
                callback_data=UserInboundsCallbacks(action=action, is_done=True).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardTexts.HOME,
                callback_data=PagesCallbacks(page=PagesActions.HOME).pack(),
            ),
        )
        return kb.adjust(2).as_markup()

    @staticmethod
    def admins(admins: list[Admin]) -> InlineKeyboardMarkup:
        """
        Generates a keyboard with buttons for each admin in the list.
        """
        kb = InlineKeyboardBuilder()

        for admin in admins:
            kb.button(
                text=admin.username,
                callback_data=AdminSelectCallbacks(username=admin.username),
            )

        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.HOME,
                callback_data=PagesCallbacks(page=PagesActions.HOME).pack(),
            ),
        )
        return kb.adjust(2).as_markup()

    @staticmethod
    def node_monitoring() -> InlineKeyboardMarkup:
        """
        Generates a keyboard for node monitoring actions, such as checking or restarting nodes.
        """
        kb = InlineKeyboardBuilder()

        kb.button(
            text=KeyboardTexts.NODE_MONITORING_CHECKER,
            callback_data=ConfirmCallbacks(
                page=BotActions.NODE_CHECKER, action=AdminActions.EDIT, is_confirm=True
            ),
        )
        kb.button(
            text=KeyboardTexts.NODE_MONITORING_AUTO_RESTART,
            callback_data=ConfirmCallbacks(
                page=BotActions.NODE_AUTO_RESTART,
                action=AdminActions.EDIT,
                is_confirm=True,
            ),
        )
        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.HOME,
                callback_data=PagesCallbacks(page=PagesActions.HOME).pack(),
            ),
        )
        return kb.adjust(2).as_markup()

    @staticmethod
    def users() -> InlineKeyboardMarkup:
        """
        Generates a keyboard with options for managing user inbounds, such as adding or deleting.
        """
        kb = InlineKeyboardBuilder()

        kb.button(
            text=KeyboardTexts.USERS_ADD_INBOUND,
            callback_data=ConfirmCallbacks(
                page=BotActions.USERS_INBOUND, action=AdminActions.ADD
            ),
        )
        kb.button(
            text=KeyboardTexts.USERS_DELETE_INBOUND,
            callback_data=ConfirmCallbacks(
                page=BotActions.USERS_INBOUND, action=AdminActions.DELETE
            ),
        )
        kb.row(
            InlineKeyboardButton(
                text=KeyboardTexts.HOME,
                callback_data=PagesCallbacks(page=PagesActions.HOME).pack(),
            ),
        )
        return kb.adjust(2).as_markup()

    @staticmethod
    def user(user: UserResponse) -> InlineKeyboardMarkup:
        """
        Generates a keyboard with a button to copy the user subscription link.
        """
        kb = InlineKeyboardBuilder()

        kb.button(
            text=KeyboardTexts.USER_CREATE_LINK_COPY,
            copy_text=CopyTextButton(text=user.subscription_url),
        )
        return kb.as_markup()
