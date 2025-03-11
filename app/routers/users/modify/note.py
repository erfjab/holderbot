from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.keys import BotKeys, SelectCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.api import ClinetManager
from app.models.user import UserModify, MarzneshinUserModify
from .base import UserModifyForm


router = Router(name="users_modify_note")


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.USERS))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [UserModify.NOTE.value],
            )
        )
    )
)
async def datestart(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        return await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )

    await state.update_data(panel=callback_data.panel)
    await state.update_data(username=callback_data.extra)
    await state.set_state(UserModifyForm.NOTE)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_NOTE,
        reply_markup=BotKeys.cancel(
            server_back=server.id, user_back=callback_data.extra
        ),
    )


@router.message(StateFilter(UserModifyForm.NOTE))
async def dateend(message: Message, state: FSMContext):
    if not message.text or len(message.text) > 500:
        track = await message.answer(text=MessageTexts.WRONG_STR)
        return await tracker.add(track)

    data = await state.get_data()

    server = await crud.get_server(int(data["panel"]))
    if not server:
        track = await message.answer(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.cleardelete(message, track)

    action = await ClinetManager.modify_user(
        server,
        data["username"],
        MarzneshinUserModify(username=data["username"], note=message.text).dict(),
    )
    track = await message.answer(
        text=MessageTexts.SUCCESS if action else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(server_back=server.id, user_back=data["username"]),
    )
    return await tracker.cleardelete(message, track)
