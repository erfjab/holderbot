import asyncio

from marzban import MarzbanAPI

from db.crud import SettingManager, TokenManager
from models.setting import SettingKeys
from utils import report
from utils.config import MARZBAN_ADDRESS, EXCLUDED_MONITORINGS

panel = MarzbanAPI(base_url=MARZBAN_ADDRESS)


async def node_checker():
    node_checker_is_active = await SettingManager.get(
        SettingKeys.NodeMonitoringIsActive
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
                SettingKeys.NodeMonitoringAutoRestart
            )
            if not node_auto_restart:
                continue

            await asyncio.sleep(2.0)

            try:
                await panel.reconnect_node(node.id, token.token)
                await report.node_restart(node, True)
            except:  # noqa: E722
                await report.node_restart(node, False)

    if anti_spam:
        await asyncio.sleep(60.0)
