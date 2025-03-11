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

router = Router(name="actions_users")


class UsersActionsForm(StatesGroup):
    ADMINS = State()
    USERS = State()


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.ACTIONS))
        & (F.action.is_(Actions.INFO))
        & (
            F.select.in_(
                [
                    ActionTypes.DELETE_LIMITED_USERS.value,
                    ActionTypes.DELETE_EXPIRED_USERS.value,
                    ActionTypes.ACTIVATED_USERS.value,
                    ActionTypes.DISABLED_USERS.value,
                    ActionTypes.DELETE_USERS.value,
                ]
            )
        )
    )
)
async def select(callback: CallbackQuery, callback_data: SelectCB, state: FSMContext):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.update_data(action=callback_data.select)
    await state.set_state(UsersActionsForm.ADMINS)
    admins = await ClinetManager.get_admins(server=server)
    if not admins:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND,
            reply_markup=BotKeys.cancel(server_back=server.id),
        )
        return await tracker.add(track)
    admins = [admin.username for admin in admins]
    if callback_data.select in [
        ActionTypes.DELETE_EXPIRED_USERS,
        ActionTypes.DELETE_LIMITED_USERS,
    ]:
        admins.append("ALL")
    return await callback.message.edit_text(
        text=MessageTexts.ASK_ADMIN,
        reply_markup=BotKeys.selector(
            data=admins,
            types=Pages.ACTIONS,
            action=Actions.INFO,
            panel=server.id,
            server_back=server.id,
        ),
    )


@router.callback_query(
    StateFilter(UsersActionsForm.ADMINS),
    SelectCB.filter((F.types.is_(Pages.ACTIONS)) & (F.action.is_(Actions.INFO))),
)
async def admins(callback: CallbackQuery, callback_data: SelectCB, state: FSMContext):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.update_data(admin=callback_data.select)
    await state.set_state(UsersActionsForm.USERS)
    return await callback.message.edit_text(
        text=MessageTexts.ITEMS,
        reply_markup=BotKeys.selector(
            data=[YesOrNot.YES, YesOrNot.NO],
            types=Pages.ACTIONS,
            action=Actions.INFO,
            panel=server.id,
            server_back=server.id,
        ),
    )


@router.callback_query(
    StateFilter(UsersActionsForm.USERS),
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
    admin = data.get("admin", None)
    action_mapping = {
        ActionTypes.DELETE_EXPIRED_USERS.value: ActionTypes.DELETE_EXPIRED_USERS,
        ActionTypes.DELETE_LIMITED_USERS.value: ActionTypes.DELETE_LIMITED_USERS,
        ActionTypes.DELETE_USERS.value: ActionTypes.DELETE_USERS,
        ActionTypes.DISABLED_USERS.value: ActionTypes.DISABLED_USERS,
        ActionTypes.ACTIVATED_USERS.value: ActionTypes.ACTIVATED_USERS,
    }
    action_type = action_mapping.get(data["action"], None)

    if action_type in [ActionTypes.ACTIVATED_USERS, ActionTypes.DISABLED_USERS]:
        result = (
            await ClinetManager.activated_users(server, admin)
            if action_type == ActionTypes.ACTIVATED_USERS
            else await ClinetManager.disabled_users(server, admin)
        )
        return await callback.message.edit_text(
            MessageTexts.SUCCESS if result else MessageTexts.FAILED,
            reply_markup=BotKeys.cancel(server_back=server.id),
        )

    page = 1
    all_users = 0
    success = 0

    async def process_user_batch(users: list[MarzneshinUserResponse]) -> int:
        tasks = [ClinetManager.remove_user(server, user.username) for user in users]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return sum(1 for r in results if r and not isinstance(r, Exception))

    while True:
        users = await ClinetManager.get_users(
            server,
            page,
            size=server.size_value,
            limited=True if action_type == ActionTypes.DELETE_LIMITED_USERS else None,
            expired=True if action_type == ActionTypes.DELETE_EXPIRED_USERS else None,
            owner_username=None if admin == "ALL" else admin,
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
