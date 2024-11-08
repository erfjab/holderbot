"""
This module contains the handlers for the node monitoring menu and actions.
It includes callbacks for toggling settings related to node monitoring.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from db.crud import SettingManager
from utils import MessageTexts, BotKeyboards, panel
from models import (
    PagesActions,
    PagesCallbacks,
    SettingKeys,
    ConfirmCallbacks,
    BotActions,
    NodeSelectCallbacks,
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
    excluded_nodes = await SettingManager.get_node_excluded()
    excluded_text = ", ".join(excluded_nodes) if excluded_nodes else "None"

    text = MessageTexts.NODE_MONITORING_MENU.format(
        checker=checker_status,
        auto_restart=auto_restart_status,
        excluded=excluded_text,
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


@router.callback_query(ConfirmCallbacks.filter(F.page.is_(BotActions.NODE_EXCLUDED)))
async def node_excluded(callback: CallbackQuery, state: FSMContext):
    """Start the process to exclude nodes from monitoring."""
    await state.clear()
    nodes = await panel.get_nodes()
    await state.set_data(
        {
            "all_nodes": [node.__dict__ for node in nodes],
            "selected_nodes": [node.name for node in nodes],
        }
    )

    return await callback.message.edit_text(
        text=MessageTexts.NODE_MONITORING_EXCLUDED,
        reply_markup=BotKeyboards.select_nodes(nodes, [node.name for node in nodes]),
    )


@router.callback_query(NodeSelectCallbacks.filter(F.is_done.is_(False)))
async def select_node_excluded(
    callback: CallbackQuery, state: FSMContext, callback_data: NodeSelectCallbacks
):
    """Toggle a node’s selection for exclusion."""
    data = await state.get_data()
    selected_nodes: list = data.get("selected_nodes", [])
    all_nodes = data.get("all_nodes", [])

    if callback_data.name in selected_nodes:
        selected_nodes.remove(callback_data.name)
    else:
        selected_nodes.append(callback_data.name)

    await state.update_data(selected_nodes=selected_nodes)

    return await callback.message.edit_text(
        text=MessageTexts.NODE_MONITORING_EXCLUDED,
        reply_markup=BotKeyboards.select_nodes(all_nodes, selected_nodes),
    )


@router.callback_query(NodeSelectCallbacks.filter(F.is_done.is_(True)))
async def finish_node_selection(callback: CallbackQuery, state: FSMContext):
    """Save the selected nodes and finish the process."""
    data = await state.get_data()
    selected_nodes = data.get("selected_nodes", [])

    await SettingManager.update_node_excluded(selected_nodes)
    await state.clear()

    return await callback.message.edit_text(
        text=MessageTexts.SUCCESS_UPDATED, reply_markup=BotKeyboards.home()
    )
