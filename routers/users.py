from aiogram import Router, F
from aiogram.types import CallbackQuery
from models import (
    PagesActions,
    PagesCallbacks,
    AdminActions,
    ConfirmCallbacks,
    BotActions,
    UserInboundsCallbacks,
)
from utils.lang import MessageTexts
from utils.keys import BotKeyboards
from utils import panel, helpers

router = Router()


@router.callback_query(PagesCallbacks.filter(F.page == PagesActions.UsersMenu))
async def menu(callback: CallbackQuery):
    return await callback.message.edit_text(
        text=MessageTexts.UsersMenu, reply_markup=BotKeyboards.users()
    )


@router.callback_query(ConfirmCallbacks.filter(F.page == BotActions.UsersInbound))
async def inbound_add(callback: CallbackQuery, callback_data: ConfirmCallbacks):
    inbounds = await panel.inbounds()
    return await callback.message.edit_text(
        text=MessageTexts.UsersInboundSelect,
        reply_markup=BotKeyboards.inbounds(
            inbounds=inbounds, action=callback_data.action, just_one_inbound=True
        ),
    )


@router.callback_query(
    UserInboundsCallbacks.filter(
        (
            F.action.in_([AdminActions.Add, AdminActions.Delete])
            & (F.is_done.is_(True))
            & (F.just_one_inbound.is_(True))
        )
    )
)
async def inbound_confirm(
    callback: CallbackQuery, callback_data: UserInboundsCallbacks
):
    working_message = await callback.message.edit_text(text=MessageTexts.Working)
    try:
        result = await helpers.manage_panel_inbounds(
            callback_data.tag,
            callback_data.protocol,
            (
                AdminActions.Add
                if callback_data.action.value == AdminActions.Add.value
                else AdminActions.Delete
            ),
        )

        return await working_message.edit_text(
            text=MessageTexts.UsersInboundSuccessUpdated if result else MessageTexts.UsersInboundErrorUpdated,
            reply_markup=BotKeyboards.home()
        )

    except Exception as e:
        return await working_message.edit_text(
            text=f"{MessageTexts.UsersInboundErrorUpdated}: {str(e)}"
        )
