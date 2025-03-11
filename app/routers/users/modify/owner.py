from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.keys import BotKeys, SelectCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.api import ClinetManager
from app.settings.track import tracker
from app.models.user import UserModify
from .base import UserModifyForm

router = Router(name="users_modify_owner")


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.USERS))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [
                    UserModify.OWNER.value,
                ]
            )
        )
    )
)
async def ownerstart(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    admins = await ClinetManager.get_admins(server=server)
    if not admins:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND,
            reply_markup=BotKeys.cancel(
                server_back=server.id, user_back=callback_data.extra
            ),
        )
        return await tracker.add(track)

    await state.set_state(UserModifyForm.ADMIN)
    await state.update_data(action=callback_data.select)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_ADMIN,
        reply_markup=BotKeys.selector(
            data=[admin.username for admin in admins],
            types=Pages.USERS,
            action=Actions.MODIFY,
            panel=server.id,
            extra=callback_data.extra,
            server_back=server.id,
            user_back=callback_data.extra,
        ),
    )


@router.callback_query(
    StateFilter(UserModifyForm.ADMIN),
    SelectCB.filter((F.types.is_(Pages.USERS)) & (F.action.is_(Actions.MODIFY))),
)
async def ownerend(callback: CallbackQuery, callback_data: SelectCB, state: FSMContext):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    action = await ClinetManager.set_owner(
        server=server, username=callback_data.extra, admin=callback_data.select
    )
    await state.clear()
    return await callback.message.edit_text(
        text=MessageTexts.SUCCESS if action else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(
            server_back=server.id, user_back=callback_data.extra
        ),
    )
