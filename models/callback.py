from aiogram.filters.callback_data import CallbackData
from enum import Enum


class AdminActions(str, Enum):
    Add = "add"
    Edit = "edit"
    Info = "info"
    Delete = "delete"


class BotActions(str, Enum):
    NodeChecker = "node_checker"
    NodeAutoRestart = "node_auto_restart"
    UsersInbound = "users_inbound"


class PagesActions(str, Enum):
    Home = "home"
    UserCreate = "user_create"
    NodeMonitoring = "node_monitoring"
    UsersMenu = "users_menu"


class PagesCallbacks(CallbackData, prefix="pages"):
    page: PagesActions


class ConfirmCallbacks(CallbackData, prefix="confim"):
    page: BotActions
    action: AdminActions
    is_confirm: bool = False


class UserStatusCallbacks(CallbackData, prefix="user_status"):
    status: str
    action: AdminActions


class UserInboundsCallbacks(CallbackData, prefix="user_inbounds"):
    tag: str | None = None
    protocol: str | None = None
    is_selected: bool | None = None
    action: AdminActions
    is_done: bool = False
    just_one_inbound: bool = False


class AdminSelectCallbacks(CallbackData, prefix="admin_select"):
    username: str
