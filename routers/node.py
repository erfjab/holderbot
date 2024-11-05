"""
This module contains the handlers for the node monitoring menu and actions.
It includes callbacks for toggling settings related to node monitoring.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from db.crud import SettingManager
from utils.lang import MessageTexts
from utils.keys import BotKeyboards
from models import (
    PagesActions,
    PagesCallbacks,
    SettingKeys,
    SettingUpsert,
    ConfirmCallbacks,
    BotActions,
)

router = Router()


async def get_setting_status(key: SettingKeys) -> str:
    """
    Returns the status of the specified setting as 'ON' or 'OFF'.
    """
    return "ON" if await SettingManager.get(key) else "OFF"


async def toggle_setting(key: SettingKeys):
    """
    Toggles the value of the specified setting.
    """
    current_value = await SettingManager.get(key)
    new_value = None if current_value else "True"
    await SettingManager.upsert(SettingUpsert(key=key, value=new_value))


@router.callback_query(PagesCallbacks.filter(F.page.is_(PagesActions.NODE_MONITORING)))
async def node_monitoring_menu(callback: CallbackQuery):
    """
    Handler for the node monitoring menu callback. It retrieves the current status
    of node monitoring settings and updates the menu text.
    """
    checker_status = await get_setting_status(SettingKeys.NODE_MONITORING_IS_ACTIVE)
    auto_restart_status = await get_setting_status(SettingKeys.NODE_MONITORING_AUTO_RESTART)

    text = MessageTexts.NODE_MONITORING_MENU.format(
        checker=checker_status,
        auto_restart=auto_restart_status,
    )
    await callback.message.edit_text(
        text=text, reply_markup=BotKeyboards.node_monitoring()
    )


@router.callback_query(ConfirmCallbacks.filter(F.page.is_(BotActions.NODE_AUTO_RESTART)))
async def node_monitoring_auto_restart(callback: CallbackQuery):
    """
    Handler for toggling the auto-restart setting for node monitoring.
    """
    await toggle_setting(SettingKeys.NODE_MONITORING_AUTO_RESTART)
    await node_monitoring_menu(callback)


@router.callback_query(ConfirmCallbacks.filter(F.page.is_(BotActions.NODE_CHECKER)))
async def node_monitoring_checker(callback: CallbackQuery):
    """
    Handler for toggling the checker setting for node monitoring.
    """
    await toggle_setting(SettingKeys.NODE_MONITORING_IS_ACTIVE)
    await node_monitoring_menu(callback)
