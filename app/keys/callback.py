from enum import Enum
from aiogram.filters.callback_data import CallbackData


class Pages(str, Enum):
    """admin page enums"""

    HOME = "home"
    SERVER = "server"


class Actions(str, Enum):
    """admin actions enums"""

    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class PageCB(CallbackData, prefix="pages"):
    """admin pages callbacks"""

    page: Pages = Pages.HOME
    action: Actions | None = None
    server: int | None = None
