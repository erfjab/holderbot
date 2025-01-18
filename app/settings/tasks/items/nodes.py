from app.api import ClinetManager
from app.db import crud
from app.settings.log import logger
from app.bot import bot
from app.settings.config import env


async def monitoring_nodes():
    text = "<b>❌ This Nodes is have a error!</b>\n"
    has_error = False
    servers = await crud.get_servers()

    for server in servers:
        if not server.node_monitoring:
            continue

        nodes = await ClinetManager.get_nodes(server)
        if not nodes:
            logger.error(f"Failed to access {server.remark} nodes!")
            continue

        for node in nodes:
            if node.is_have_error:
                has_error = True
                text += (
                    f"➖➖➖➖➖\n"
                    f"<b>Node Remark:</b> <code>{node.remark}</code>\n"
                    f"<b>Node Address:</b> <code>{node.address}</code>\n"
                    f"<b>Node Message:</b> <code>{node.message}</code>\n"
                )
                if server.node_restart:
                    await ClinetManager.restart_node(server, node.id)
                    text += "<b>Node Is Restart:</b> <code>✔️</code>\n"

    if has_error:
        for admin in env.TELEGRAM_ADMINS_ID:
            await bot.send_message(
                chat_id=admin,
                text=text,
            )
