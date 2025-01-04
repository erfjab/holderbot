from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keys import BotKeys, PageCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.api import ClinetManager

router = Router(name="users_menu")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.USERS)) & (F.action.is_(Actions.LIST)))
)
async def data(callback: CallbackQuery, callback_data: PageCB):
    server = await crud.get_server(callback_data.panel)
    if not server:
        return await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
    users = await ClinetManager.get_users(
        server=server, page=callback_data.pagenumber or 1, size=10
    )
    if not users:
        return await callback.answer(text=MessageTexts.NOT_FOUND, show_alert=True)

    current = callback_data.pagenumber
    has_more = len(users) == 10

    control = (
        current - 1 if current else 0,
        current + 1 if has_more and current else (2 if not current else 0),
    )

    return await callback.message.edit_text(
        text=MessageTexts.ITEMS_MENU,
        reply_markup=BotKeys.lister(
            items=users,
            page=Pages.USERS,
            panel=server.id,
            control=control,
        ),
    )
