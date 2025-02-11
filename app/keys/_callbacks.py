from enum import Enum
from aiogram.filters.callback_data import CallbackData

from ._enums import Pages, Actions


class PageCB(CallbackData, prefix="pages"):
    page: Pages = Pages.HOME
    action: Actions = Actions.LIST
    dataid: int | str | None = None
    datatype: str | Enum | None = None
    panel: int | None = None
    pagenumber: int | None = None
    filters: str | None = None


class SelectCB(CallbackData, prefix="select"):
    select: str | int | Enum | None = None
    types: Pages
    action: Actions | None = None
    selected: bool | None = None
    done: bool = False
    panel: int | None = None
    extra: str | None = None
