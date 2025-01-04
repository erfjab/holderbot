from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keys import BotKeys, PageCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts

router = Router(name="server_data")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.SERVERS)) & (F.action.is_(Actions.INFO)))
)
async def data(callback: CallbackQuery, callback_data: PageCB):
    server = await crud.get_server(callback_data.panel)
    if not server:
        return await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )

    return await callback.message.edit_text(
        text=server.format_data,
        reply_markup=BotKeys.cancel(),
    )
