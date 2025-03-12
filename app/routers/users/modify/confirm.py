from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.keys import BotKeys, SelectCB, Pages, Actions, YesOrNot
from app.db import crud
from app.settings.utils.qrcode import create_qr
from app.settings.language import MessageTexts
from app.api import ClinetManager
from app.settings.track import tracker
from app.models.user import UserModify
from .base import UserModifyForm


router = Router(name="users_modify_confirms")


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
            server_back=server.id,
            user_back=callback_data.extra,
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
            text=MessageTexts.FAILED,
            reply_markup=BotKeys.cancel(
                server_back=callback_data.panel, user_back=callback_data.extra
            ),
        )
        return await tracker.add(track)

    data = await state.get_data()

    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)
    keyboard = BotKeys.cancel(server_back=server.id, user_back=callback_data.extra)
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
            if action:
                await callback.message.answer_photo(
                    photo=BufferedInputFile(
                        file=await create_qr(action.subscription_url),
                        filename="holderbot.png",
                    ),
                    caption=MessageTexts.USER_INFO.format(**action.format_data),
                )

        case UserModify.REMOVE:
            action = await ClinetManager.remove_user(
                server=server, username=callback_data.extra
            )
            if action:
                keyboard = BotKeys.cancel(server_back=server.id)
    return await callback.message.edit_text(
        text=MessageTexts.SUCCESS if action else MessageTexts.FAILED,
        reply_markup=keyboard,
    )
