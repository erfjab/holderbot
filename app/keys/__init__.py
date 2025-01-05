from ._callbacks import PageCB, SelectCB
from ._enums import (
    Pages,
    Actions,
)
from .manager import _KeyboardsManager

BotKeys = _KeyboardsManager()

__all__ = ["BotKeys", "Pages", "Actions", "PageCB", "SelectCB"]
