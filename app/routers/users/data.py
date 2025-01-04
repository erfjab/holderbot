from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from app.keys import BotKeys, PageCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.api import ClinetManager
from app.settings.utils.qrcode import create_qr

router = Router(name="users_data")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.USERS)) & (F.action.is_(Actions.INFO)))
)
async def data(callback: CallbackQuery, callback_data: PageCB):
    server = await crud.get_server(callback_data.panel)
    if not server:
        return await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
    user = await ClinetManager.get_user(server, callback_data.dataid)
    if not user:
        return await callback.answer(text=MessageTexts.NOT_FOUND, show_alert=True)
    return await callback.message.answer_photo(
        photo=BufferedInputFile(
            await create_qr(user.subscription_url), filename="holderbot.png"
        ),
        caption=user.format_data,
        reply_markup=BotKeys.cancel(),
    )
