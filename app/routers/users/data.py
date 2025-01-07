from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keys import BotKeys, PageCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.api import ClinetManager
from app.settings.track import tracker
from app.models.user import UserModify

router = Router(name="users_data")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.USERS)) & (F.action.is_(Actions.INFO)))
)
async def data(callback: CallbackQuery, callback_data: PageCB):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    user = await ClinetManager.get_user(server, callback_data.dataid)
    if not user:
        return await callback.answer(text=MessageTexts.NOT_FOUND, show_alert=True)

    return await callback.message.edit_text(
        text=user.format_data_str(),
        reply_markup=BotKeys.selector(
            data=[
                UserModify.ACTIVATED,
                UserModify.DISABLED,
                UserModify.RESET_USAGE,
                UserModify.REVOKE,
                UserModify.QRCODE,
                UserModify.REMOVE,
            ],
            types=Pages.USERS,
            action=Actions.MODIFY,
            extra=user.username,
            panel=server.id,
        ),
    )
