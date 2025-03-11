import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keys import BotKeys, SelectCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.models.action import ActionTypes
from app.api import ClinetManager
from app.api.types.marzneshin import MarzneshinUserResponse

router = Router(name="actions_add_config")


class ConfigsActionsForm(StatesGroup):
    ADMINS = State()
    CONFIGS = State()


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.ACTIONS))
        & (F.action.is_(Actions.INFO))
        & (
            F.select.in_(
                [ActionTypes.ADD_CONFIG.value, ActionTypes.DELETE_CONFIG.value]
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

    await state.set_state(ConfigsActionsForm.ADMINS)
    admins = await ClinetManager.get_admins(server=server)
    if not admins:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND,
            reply_markup=BotKeys.cancel(server_back=server.id),
        )
        return await tracker.add(track)

    await state.update_data(action=callback_data.select)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_ADMIN,
        reply_markup=BotKeys.selector(
            data=[admin.username for admin in admins] + ["ALL"],
            types=Pages.ACTIONS,
            action=Actions.INFO,
            panel=server.id,
            server_back=server.id,
        ),
    )


@router.callback_query(
    StateFilter(ConfigsActionsForm.ADMINS),
    SelectCB.filter((F.types.is_(Pages.ACTIONS)) & (F.action.is_(Actions.INFO))),
)
async def admin(callback: CallbackQuery, callback_data: SelectCB, state: FSMContext):
    await state.update_data(admin=callback_data.select)

    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.set_state(ConfigsActionsForm.CONFIGS)
    configs = await ClinetManager.get_configs(server)
    if not configs:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND,
            reply_markup=BotKeys.cancel(server_back=server.id),
        )
        return await tracker.add(track)

    await state.update_data(configs=[config.dict() for config in configs])
    return await callback.message.edit_text(
        text=MessageTexts.ITEMS,
        reply_markup=BotKeys.selector(
            data=[config.remark for config in configs],
            types=Pages.ACTIONS,
            action=Actions.INFO,
            panel=server.id,
            width=1,
            server_back=server.id,
        ),
    )


@router.callback_query(
    StateFilter(ConfigsActionsForm.CONFIGS),
    SelectCB.filter((F.types.is_(Pages.ACTIONS)) & (F.action.is_(Actions.INFO))),
)
async def action(callback: CallbackQuery, callback_data: SelectCB, state: FSMContext):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    data = await state.get_data()
    configs = data["configs"]
    selected = callback_data.select
    target_config = next(
        (config for config in configs if config["remark"] == selected), None
    )
    if not target_config:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND,
            reply_markup=BotKeys.cancel(server_back=server.id),
        )
        return await tracker.add(track)

    await callback.message.edit_text(text="⏳")

    target = int(target_config["id"])
    action_type = data["action"]

    global all_users

    async def process_user(user: MarzneshinUserResponse):
        global all_users
        if action_type == ActionTypes.ADD_CONFIG.value:
            if target not in user.service_ids:
                user.service_ids.append(target)
                all_users += 1
            else:
                return False
        elif action_type == ActionTypes.DELETE_CONFIG.value:
            if target in user.service_ids:
                user.service_ids.remove(target)
                all_users += 1

            else:
                return False

        modify = await ClinetManager.modify_user(
            server=server,
            username=user.username,
            data={
                "username": user.username,
                "service_ids": user.service_ids,
            },
        )
        return modify

    page = 1
    all_users = 0
    success = 0

    while True:
        adminselect = data["admin"]
        users = await ClinetManager.get_users(
            server,
            page,
            size=server.size_value,
            owner_username=None if adminselect == "ALL" else adminselect,
        )
        if not users:
            break

        results = await asyncio.gather(*(process_user(user) for user in users))
        success += sum(1 for result in results if result)

        page += 1

    track = await callback.message.answer(
        text=f"Action Finished: {success}/{all_users}",
        reply_markup=BotKeys.cancel(server_back=server.id),
    )
    return await tracker.cleardelete(callback, track)
