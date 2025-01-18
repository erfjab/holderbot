from app.api import ClinetManager
from app.db import crud
from app.settings.log import logger
from app.bot import bot
from app.settings.config import env


async def monitoring_nodes():
    servers = await crud.get_servers()
    for server in servers:
        nodes = await ClinetManager.get_nodes(server)
        if not nodes:
            logger.error(f"Failed to access {server.remark} nodes!")
            continue
        for node in nodes:
            if node.is_have_error:
                logger.info(f"node {node.remark} | {node.address} | {node.message}")
                for admin in env.TELEGRAM_ADMINS_ID:
                    await bot.send_message(
                        chat_id=admin,
                        text=(
                            f"{node.remark} node is have a error!\n"
                            f"node address: {node.address}\n"
                            f"node message: {node.message}\n"
                        ),
                    )
                    await ClinetManager.restart_node(server, node.id)
