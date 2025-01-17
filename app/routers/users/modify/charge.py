from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.keys import BotKeys, SelectCB, Pages, Actions, YesOrNot
from app.db import crud
from app.settings.language import MessageTexts
from app.api import ClinetManager
from app.settings.track import tracker
from app.models.user import UserModify
from app.settings.utils.user import charge_user_data
from .base import UserModifyForm

router = Router(name="users_modify_charge")


@router.callback_query(
    SelectCB.filter(
        (F.types.is_(Pages.USERS))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [
                    UserModify.CHARGE.value,
                ]
            )
        )
    )
)
async def chargestart(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    templates = await crud.get_templates(active=True)
    if not templates:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.set_state(UserModifyForm.TEMPLATE)
    await state.update_data(username=callback_data.extra)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_ADMIN,
        reply_markup=BotKeys.selector(
            data=[tem.button_remark for tem in templates],
            types=Pages.USERS,
            action=Actions.MODIFY,
            panel=server.id,
            extra=callback_data.extra,
            width=1,
        ),
    )


@router.callback_query(
    StateFilter(UserModifyForm.TEMPLATE),
    SelectCB.filter((F.types.is_(Pages.USERS)) & (F.action.is_(Actions.MODIFY))),
)
async def chargeend(
    callback: CallbackQuery, callback_data: SelectCB, state: FSMContext
):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await state.update_data(templateid=callback_data.select.split()[0])
    await state.set_state(UserModifyForm.CHARGE)
    return await callback.message.edit_text(
        text=MessageTexts.ASK_SURE,
        reply_markup=BotKeys.selector(
            data=[YesOrNot.YES_USAGE, YesOrNot.YES, YesOrNot.NO],
            types=Pages.USERS,
            action=Actions.MODIFY,
            extra=callback_data.extra,
            panel=server.id,
        ),
    )


@router.callback_query(
    StateFilter(UserModifyForm.CHARGE),
    SelectCB.filter(
        (F.types.is_(Pages.USERS))
        & (F.action.is_(Actions.MODIFY))
        & (
            F.select.in_(
                [
                    YesOrNot.YES_USAGE,
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
    template = await crud.get_template(int(data["templateid"]))
    if not template:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    if callback_data.select == YesOrNot.YES_USAGE.value:
        await ClinetManager.reset_user(server, data["username"])

    datadict = charge_user_data(
        server.types,
        data["username"],
        template.data_limit,
        template.date_limit,
        template.date_types,
    )
    action = await ClinetManager.modify_user(server, data["username"], datadict)
    return await callback.message.edit_text(
        text=MessageTexts.SUCCESS if action else MessageTexts.FAILED,
        reply_markup=BotKeys.cancel(),
    )
