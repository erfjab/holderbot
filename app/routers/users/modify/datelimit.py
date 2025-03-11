from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.keys import BotKeys, SelectCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.api import ClinetManager
from app.models.user import (
    UserModify,
    DateTypes,
)
from app.settings.utils.user import charge_user_datelimit
from .base import UserModifyForm


router = Router(name="users_modify_date_limit")


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.USERS))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [UserModify.DATE_LIMIT.value],
            )
        )
    )
)
async def selecttype(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        return await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )

    await state.set_state(UserModifyForm.DATE_TYPE)
    return await callback.message.edit_text(
        text=MessageTexts.MENU,
        reply_markup=BotKeys.selector(
            data=[DateTypes.UNLIMITED, DateTypes.NOW, DateTypes.AFTER_FIRST_USE],
            types=Pages.USERS,
            action=Actions.MODIFY,
            width=1,
            panel=callback_data.panel,
            extra=callback_data.extra,
            server_back=server.id,
            user_back=callback_data.extra,
        ),
    )


@router.callback_query(
    StateFilter(UserModifyForm.DATE_TYPE),
    SelectCB.filter((F.types.is_(Pages.USERS)) & (F.action.is_(Actions.MODIFY))),
)
async def datelimit(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    if callback_data.select == DateTypes.UNLIMITED:
        server = await crud.get_server(callback_data.panel)
        if not server:
            return await callback.message.edit_text(
                text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
            )
        datadict = charge_user_datelimit(
            server.types, callback_data.extra, 0, DateTypes.UNLIMITED
        )
        action = await ClinetManager.modify_user(
            server=server,
            username=callback_data.extra,
            data=datadict,
        )
        await state.clear()
        return await callback.message.edit_text(
            text=MessageTexts.SUCCESS if action else MessageTexts.FAILED,
            reply_markup=BotKeys.cancel(
                server_back=server.id, user_back=callback_data.extra
            ),
        )

    else:
        await state.update_data(username=callback_data.extra)
        await state.update_data(panel=callback_data.panel)
        await state.update_data(datetypes=callback_data.select)
        await state.set_state(UserModifyForm.DATE_LIMIT)
        return await callback.message.edit_text(
            text=MessageTexts.ASK_DATE_LIMIT,
            reply_markup=BotKeys.cancel(
                server_back=callback_data.panel, user_back=callback_data.extra
            ),
        )


@router.message(StateFilter(UserModifyForm.DATE_LIMIT))
async def dateend(message: Message, state: FSMContext):
    if not message.text.isdigit() and int(message.text) <= 0:
        track = await message.answer(text=MessageTexts.WRONG_INT)
        return await tracker.add(track)

    server = await crud.get_server(await state.get_value("panel"))
    if not server:
        track = await message.answer(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    data = await state.get_data()
    datadict = charge_user_datelimit(
        server.types, data["username"], message.text, data["datetypes"]
    )
    action = await ClinetManager.modify_user(
        server=server,
        username=data["username"],
        data=datadict,
    )
    await state.clear()
    track = await message.answer(
        text=MessageTexts.SUCCESS if action else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(server_back=server.id, user_back=data["username"]),
    )
    return await tracker.cleardelete(message, track)
