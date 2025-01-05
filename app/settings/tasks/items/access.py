from app.api import ClinetManager
from app.db import crud
from app.settings.log import logger


async def access_generate():
    servers = await crud.get_servers()
    for server in servers:
        access = await ClinetManager.generate_access(server.data, server.types)
        if not access:
            logger.warning("Failed to generate access: %s", server.remark)
            return
        await crud.upsert_server_access(serverid=server.id, serveraccess=access)
