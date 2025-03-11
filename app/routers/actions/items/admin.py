import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.api.types.marzneshin import MarzneshinUserResponse

from app.keys import BotKeys, SelectCB, Pages, Actions, YesOrNot
from app.db import crud
from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.models.action import ActionTypes
from app.api import ClinetManager

router = Router(name="actions_admin")


class AdminActionsForm(StatesGroup):
    FROM = State()
    TO = State()
    CONFIRM = State()


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.ACTIONS))
        & (F.action.is_(Actions.INFO))
        & (
            F.select.in_(
                [
                    ActionTypes.TRANSFER_USERS.value,
                ]
            )
        )
    )
)
async def fromadmin(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.update_data(action=callback_data.select)
    await state.set_state(AdminActionsForm.FROM)
    admins = await ClinetManager.get_admins(server=server)
    if not admins:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND,
            reply_markup=BotKeys.cancel(server_back=server.id),
        )
        return await tracker.add(track)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_ADMIN_FROM,
        reply_markup=BotKeys.selector(
            data=[admin.username for admin in admins],
            types=Pages.ACTIONS,
            action=Actions.INFO,
            panel=server.id,
            server_back=server.id,
        ),
    )


@router.callback_query(
    StateFilter(AdminActionsForm.FROM),
    SelectCB.filter((F.types.is_(Pages.ACTIONS)) & (F.action.is_(Actions.INFO))),
)
async def toadmin(callback: CallbackQuery, callback_data: SelectCB, state: FSMContext):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.update_data(fromadmin=callback_data.select)
    admins = await ClinetManager.get_admins(server=server)
    if not admins:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND,
            reply_markup=BotKeys.cancel(server_back=server.id),
        )
        return await tracker.add(track)
    await state.set_state(AdminActionsForm.TO)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_ADMIN_TO,
        reply_markup=BotKeys.selector(
            data=[admin.username for admin in admins],
            types=Pages.ACTIONS,
            action=Actions.INFO,
            panel=server.id,
            server_back=server.id,
        ),
    )


@router.callback_query(
    StateFilter(AdminActionsForm.TO),
    SelectCB.filter((F.types.is_(Pages.ACTIONS)) & (F.action.is_(Actions.INFO))),
)
async def confrimaction(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.update_data(toadmin=callback_data.select)
    await state.set_state(AdminActionsForm.CONFIRM)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_SURE,
        reply_markup=BotKeys.selector(
            data=[YesOrNot.YES, YesOrNot.NO],
            types=Pages.ACTIONS,
            action=Actions.INFO,
            panel=server.id,
            server_back=server.id,
        ),
    )


@router.callback_query(
    StateFilter(AdminActionsForm.CONFIRM),
    SelectCB.filter((F.types.is_(Pages.ACTIONS)) & (F.action.is_(Actions.INFO))),
)
async def action(callback: CallbackQuery, callback_data: SelectCB, state: FSMContext):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    if callback_data.select == YesOrNot.NO.value:
        track = await callback.message.edit_text(
            text=MessageTexts.FAILED, reply_markup=BotKeys.cancel(server_back=server.id)
        )
        return await tracker.add(track)

    await callback.message.edit_text(text="⏳")
    data = await state.get_data()
    fromadmin = data.get("fromadmin", None)
    toadmin = data.get("toadmin", None)

    page = 1
    all_users = 0
    success = 0

    async def process_user_batch(users: list[MarzneshinUserResponse]) -> int:
        tasks = [
            ClinetManager.set_owner(server, user.username, toadmin) for user in users
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return sum(1 for r in results if r and not isinstance(r, Exception))

    while True:
        users = await ClinetManager.get_users(
            server,
            page,
            size=server.size_value,
            owner_username=fromadmin,
        )

        if not users:
            break

        all_users += len(users)

        batch_success = await process_user_batch(users)
        success += batch_success

        page += 1
        await asyncio.sleep(0.01)

    track = await callback.message.answer(
        text=f"Action Finished: {success}/{all_users}",
        reply_markup=BotKeys.cancel(server_back=server.id),
    )
    return await tracker.cleardelete(callback, track)
