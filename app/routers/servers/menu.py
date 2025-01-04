from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.settings.language import MessageTexts
from app.keys import BotKeys, Pages, PageCB, Actions
from app.db import crud

router = Router(name="servers_menu")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.SERVERS)) & (F.action.is_(Actions.LIST)))
)
async def menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    servers = await crud.get_servers()
    return await callback.message.edit_text(
        text=MessageTexts.ITEMS_MENU,
        reply_markup=BotKeys.lister(servers, Pages.SERVERS),
    )
