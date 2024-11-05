"""
This module handles monitoring of nodes in the Marzban panel, including error reporting 
and automatic restarts if configured.
"""

import asyncio
from marzban import MarzbanAPI

from db.crud import SettingManager, TokenManager
from models.setting import SettingKeys
from utils import report
from utils.config import MARZBAN_ADDRESS, EXCLUDED_MONITORINGS

panel = MarzbanAPI(base_url=MARZBAN_ADDRESS)


async def node_checker():
    """Check the status of nodes and perform actions based on their status."""
    node_checker_is_active = await SettingManager.get(
        SettingKeys.NODE_MONITORING_IS_ACTIVE
    )
    if not node_checker_is_active:
        return

    token = await TokenManager.get()
    if not token:
        return

    nodes = await panel.get_nodes(token.token)
    anti_spam = False
    for node in nodes:
        if node.name in EXCLUDED_MONITORINGS:
            continue

        if node.status in ["connecting", "error"]:
            anti_spam = True
            await report.node_error(node)

            node_auto_restart = await SettingManager.get(
                SettingKeys.NODE_MONITORING_AUTO_RESTART
            )
            if not node_auto_restart:
                continue

            await asyncio.sleep(2.0)

            try:
                await panel.reconnect_node(node.id, token.token)
                await report.node_restart(node, True)
            except (ConnectionError, TimeoutError):  # Omit the variable if not used
                await report.node_restart(node, False)

    if anti_spam:
        await asyncio.sleep(60.0)
