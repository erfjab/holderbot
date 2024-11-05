"""
Module defining callback data classes for handling bot actions and page navigation.
"""

from enum import Enum
from aiogram.filters.callback_data import CallbackData


class AdminActions(str, Enum):
    """
    Enum representing various admin actions that can be performed.
    """

    ADD = "add"
    EDIT = "edit"
    INFO = "info"
    DELETE = "delete"


class BotActions(str, Enum):
    """
    Enum representing various bot actions.
    """

    NODE_CHECKER = "node_checker"
    NODE_AUTO_RESTART = "node_auto_restart"
    USERS_INBOUND = "users_inbound"


class PagesActions(str, Enum):
    """
    Enum representing different pages in the bot navigation.
    """

    HOME = "home"
    USER_CREATE = "user_create"
    NODE_MONITORING = "node_monitoring"
    USERS_MENU = "users_menu"


class PagesCallbacks(CallbackData, prefix="pages"):
    """
    Callback data structure for page navigation.
    """

    page: PagesActions


class ConfirmCallbacks(CallbackData, prefix="confirm"):
    """
    Callback data structure for confirmation actions.
    """

    page: BotActions
    action: AdminActions
    is_confirm: bool = False


class UserStatusCallbacks(CallbackData, prefix="user_status"):
    """
    Callback data structure for user status actions.
    """

    status: str
    action: AdminActions


class UserInboundsCallbacks(CallbackData, prefix="user_inbounds"):
    """
    Callback data structure for user inbounds actions.
    """

    tag: str | None = None
    protocol: str | None = None
    is_selected: bool | None = None
    action: AdminActions
    is_done: bool = False
    just_one_inbound: bool = False


class AdminSelectCallbacks(CallbackData, prefix="admin_select"):
    """
    Callback data structure for selecting an admin by username.
    """

    username: str
