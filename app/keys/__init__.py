from ._callbacks import PageCB, SelectCB
from ._enums import Pages, Actions, YesOrNot, SelectAll, JsonHandler, RandomHandler
from .manager import _KeyboardsManager

BotKeys = _KeyboardsManager()

__all__ = [
    "BotKeys",
    "Pages",
    "Actions",
    "PageCB",
    "SelectCB",
    "YesOrNot",
    "SelectAll",
    "JsonHandler",
    "RandomHandler",
]
