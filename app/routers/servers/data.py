from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.keys import BotKeys, Pages, PageCB, Actions
from app.db import crud

router = Router(name="servers_menu")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.SERVERS)) & (F.action.is_(Actions.INFO)))
)
async def menu(callback: CallbackQuery, callback_data: PageCB, state: FSMContext):
    await state.clear()
    server = await crud.get_server(key=callback_data.dataid)
    return await callback.message.edit_text(
        text=server.format_data, reply_markup=BotKeys.cancel()
    )
