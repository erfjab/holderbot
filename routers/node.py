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
    BotActions
)

router = Router()

async def get_setting_status(key: SettingKeys) -> str:
    return "ON" if await SettingManager.get(key) else "OFF"

async def toggle_setting(key: SettingKeys):
    current_value = await SettingManager.get(key)
    new_value = None if current_value else "True"
    await SettingManager.upsert(SettingUpsert(key=key, value=new_value))

@router.callback_query(PagesCallbacks.filter(F.page.is_(PagesActions.NodeMonitoring)))
async def node_monitoring_menu(callback: CallbackQuery):
    checker_status = await get_setting_status(SettingKeys.NodeMonitoringIsActive)
    auto_restart_status = await get_setting_status(SettingKeys.NodeMonitoringAutoRestart)
    
    text = MessageTexts.NodeMonitoringMenu.format(
        checker=checker_status,
        auto_restart=auto_restart_status,
    )
    await callback.message.edit_text(
        text=text, reply_markup=BotKeyboards.node_monitoring()
    )

@router.callback_query(ConfirmCallbacks.filter(F.page.is_(BotActions.NodeAutoRestart)))
async def node_monitoring_auto_restart(callback: CallbackQuery):
    await toggle_setting(SettingKeys.NodeMonitoringAutoRestart)
    await node_monitoring_menu(callback)

@router.callback_query(ConfirmCallbacks.filter(F.page.is_(BotActions.NodeChecker)))
async def node_monitoring_checker(callback: CallbackQuery):
    await toggle_setting(SettingKeys.NodeMonitoringIsActive)
    await node_monitoring_menu(callback)