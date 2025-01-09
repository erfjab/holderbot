from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.keys import BotKeys, SelectCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.api import ClinetManager
from app.settings.track import tracker
from app.models.user import UserModify, MarzneshinUserModify
from .base import UserModifyForm

router = Router(name="users_modify_configs")


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.USERS))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [
                    UserModify.CONFIGS.value,
                ]
            )
        )
    )
)
async def configstart(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    configs = await ClinetManager.get_configs(server=server)
    if not configs:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.update_data(panel=server.id)
    await state.update_data(configs=[config.dict() for config in configs])
    await state.update_data(selects=[config.dict() for config in configs])
    await state.set_state(UserModifyForm.CONFIGS)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_CONFIGS,
        reply_markup=BotKeys.selector(
            data=[config.name for config in configs],
            types=Pages.USERS,
            action=Actions.MODIFY,
            selects=[config.name for config in configs],
            panel=server.id,
            extra=callback_data.extra,
        ),
    )


@router.callback_query(
    StateFilter(UserModifyForm.CONFIGS),
    SelectCB.filter((F.types.is_(Pages.USERS)) & (F.action.is_(Actions.MODIFY))),
)
async def configselect(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    data = await state.get_data()
    selects: list[dict] = data["selects"]
    if callback_data.done is True:
        server = await crud.get_server(callback_data.panel)
        if not server:
            track = await callback.message.edit_text(
                text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
            )
            return await tracker.add(track)

        action = await ClinetManager.modify_user(
            server=server,
            username=callback_data.extra,
            data=MarzneshinUserModify(
                username=callback_data.extra,
                service_ids=[int(service["id"]) for service in selects],
            ).dict(),
        )
        await state.clear()
        return await callback.message.edit_text(
            text=MessageTexts.SUCCESS if action else MessageTexts.FAILED,
            reply_markup=BotKeys.cancel(),
        )

    configs: list[dict] = data["configs"]
    selected = callback_data.select

    target_config = next(config for config in configs if config["name"] == selected)

    if selected in {select["name"] for select in selects}:
        selects = [select for select in selects if select["name"] != selected]
    else:
        selects.append(target_config)

    await state.update_data(selects=selects)

    return await callback.message.edit_text(
        text=MessageTexts.ASK_CONFIGS,
        reply_markup=BotKeys.selector(
            data=[config["name"] for config in configs],
            types=Pages.USERS,
            action=Actions.MODIFY,
            selects=[select["name"] for select in selects],
            panel=int(data["panel"]),
            extra=callback_data.extra,
        ),
    )
