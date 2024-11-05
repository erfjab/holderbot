"""
This module contains the callback functions for managing user actions,
such as navigating the users menu, adding or deleting inbounds, and updating 
user settings related to inbounds.
"""

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


@router.callback_query(PagesCallbacks.filter(F.page == PagesActions.USERS_MENU))
async def menu(callback: CallbackQuery):
    """
    Handles the callback for the Users Menu page and displays the corresponding menu.
    """
    return await callback.message.edit_text(
        text=MessageTexts.USERS_MENU, reply_markup=BotKeyboards.users()
    )


@router.callback_query(ConfirmCallbacks.filter(F.page == BotActions.USERS_INBOUND))
async def inbound_add(callback: CallbackQuery, callback_data: ConfirmCallbacks):
    """
    Handles the callback for adding or managing inbounds in the users' settings.
    Displays the inbound selection menu based on the provided callback data.
    """
    inbounds = await panel.get_inbounds()
    return await callback.message.edit_text(
        text=MessageTexts.USERS_INBOUND_SELECT,
        reply_markup=BotKeyboards.inbounds(
            inbounds=inbounds, action=callback_data.action, just_one_inbound=True
        ),
    )


@router.callback_query(
    UserInboundsCallbacks.filter(
        (
            F.action.in_([AdminActions.ADD, AdminActions.DELETE])
            & (F.is_done.is_(True))
            & (F.just_one_inbound.is_(True))
        )
    )
)
async def inbound_confirm(
    callback: CallbackQuery, callback_data: UserInboundsCallbacks
):
    """
    Confirms the addition or deletion of an inbound for the user based on the 
    selected action. After processing the action, it updates the message with the result.
    """
    working_message = await callback.message.edit_text(text=MessageTexts.WORKING)
    result = await helpers.manage_panel_inbounds(
        callback_data.tag,
        callback_data.protocol,
        (
            AdminActions.ADD
            if callback_data.action.value == AdminActions.ADD.value
            else AdminActions.DELETE
        ),
    )

    return await working_message.edit_text(
    text=(MessageTexts.USERS_INBOUND_SUCCESS_UPDATED
          if result
          else MessageTexts.USERS_INBOUND_ERROR_UPDATED),
    reply_markup=BotKeyboards.home(),
    )
