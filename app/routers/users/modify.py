from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keys import BotKeys, SelectCB, Pages, Actions, YesOrNot
from app.db import crud
from app.settings.utils.qrcode import create_qr
from app.settings.language import MessageTexts
from app.api import ClinetManager
from app.settings.track import tracker
from app.models.user import UserModify, MarzneshinUserModify

router = Router(name="users_modify")


class UserModifyForm(StatesGroup):
    ADMIN = State()
    CONFIRM = State()
    INPUT = State()
    CONFIGS = State()


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.USERS))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [
                    UserModify.ACTIVATED.value,
                    UserModify.DISABLED.value,
                    UserModify.RESET_USAGE.value,
                    UserModify.REMOVE.value,
                    UserModify.REVOKE.value,
                    UserModify.QRCODE.value,
                ]
            )
        )
    )
)
async def confirmstart(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    if callback_data.select == UserModify.QRCODE.value:
        user = await ClinetManager.get_user(server, callback_data.extra)
        if not user:
            return await callback.answer(text=MessageTexts.NOT_FOUND, show_alert=True)

        return await callback.message.answer_photo(
            photo=BufferedInputFile(
                file=await create_qr(user.subscription_url), filename="holderbot.png"
            ),
            caption=MessageTexts.USER_INFO.format(**user.format_data),
        )

    await state.update_data(action=callback_data.select)
    await state.set_state(UserModifyForm.CONFIRM)

    return await callback.message.edit_text(
        text=MessageTexts.ASK_SURE,
        reply_markup=BotKeys.selector(
            data=[YesOrNot.YES, YesOrNot.NO],
            types=Pages.USERS,
            action=Actions.MODIFY,
            extra=callback_data.extra,
            panel=server.id,
        ),
    )


@router.callback_query(
    StateFilter(UserModifyForm.CONFIRM),
    SelectCB.filter(
        (F.types.is_(Pages.USERS))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [
                    YesOrNot.YES,
                    YesOrNot.NO,
                ]
            )
        )
    ),
)
async def confirmend(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    if callback_data.select == YesOrNot.NO.value:
        track = await callback.message.edit_text(
            text=MessageTexts.FAILED, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    data = await state.get_data()

    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    match data["action"]:
        case UserModify.DISABLED:
            action = await ClinetManager.disabled_user(
                server=server, username=callback_data.extra
            )

        case UserModify.ACTIVATED:
            action = await ClinetManager.activated_user(
                server=server, username=callback_data.extra
            )

        case UserModify.RESET_USAGE:
            action = await ClinetManager.reset_user(
                server=server, username=callback_data.extra
            )

        case UserModify.REVOKE:
            action = await ClinetManager.revoke_user(
                server=server, username=callback_data.extra
            )

        case UserModify.REMOVE:
            action = await ClinetManager.remove_user(
                server=server, username=callback_data.extra
            )

    return await callback.message.edit_text(
        text=MessageTexts.SUCCESS if action else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(),
    )


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
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
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
        reply_markup=BotKeys.cancel(),
    )


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
