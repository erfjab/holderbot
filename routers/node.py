"""
This module contains the handlers for the node monitoring menu and actions.
It includes callbacks for toggling settings related to node monitoring.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from db.crud import SettingManager
from utils import MessageTexts, BotKeyboards
from models import (
    PagesActions,
    PagesCallbacks,
    SettingKeys,
    ConfirmCallbacks,
    BotActions,
)

router = Router()


@router.callback_query(PagesCallbacks.filter(F.page.is_(PagesActions.NODE_MONITORING)))
async def node_monitoring_menu(callback: CallbackQuery):
    """
    Handler for the node monitoring menu callback. It retrieves the current status
    of node monitoring settings and updates the menu text.
    """
    checker_status = await SettingManager.get(SettingKeys.NODE_MONITORING)
    auto_restart_status = await SettingManager.get(SettingKeys.NODE_AUTO_RESTART)

    text = MessageTexts.NODE_MONITORING_MENU.format(
        checker=checker_status,
        auto_restart=auto_restart_status,
    )
    await callback.message.edit_text(
        text=text, reply_markup=BotKeyboards.node_monitoring()
    )


@router.callback_query(
    ConfirmCallbacks.filter(F.page.is_(BotActions.NODE_AUTO_RESTART))
)
async def node_monitoring_auto_restart(callback: CallbackQuery):
    """
    Handler for toggling the auto-restart setting for node monitoring.
    """
    await SettingManager.toggle_field(SettingKeys.NODE_AUTO_RESTART)
    await node_monitoring_menu(callback)


@router.callback_query(ConfirmCallbacks.filter(F.page.is_(BotActions.NODE_CHECKER)))
async def node_monitoring_checker(callback: CallbackQuery):
    """
    Handler for toggling the checker setting for node monitoring.
    """
    await SettingManager.toggle_field(SettingKeys.NODE_MONITORING)
    await node_monitoring_menu(callback)
