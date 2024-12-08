from sqlalchemy import select
from typing import Optional, Union
from .models import Server
from .base import get_db
from holderbot.models.server import ServerType, MarzServerData


async def get_servers(
    type: Optional[ServerType] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> list[Server]:
    """Get all servers from the database with optional filtering and pagination."""
    async with get_db() as db:
        query = select(Server)

        if type:
            query = query.where(Server.type == type)

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        result = await db.execute(query)
        return result.scalars().all()


async def get_server(key: Union[str, int]) -> Optional[Server]:
    """Get a specific server data with remark or id."""
    async with get_db() as db:
        query = select(Server)

        if isinstance(key, str):
            query = query.where(Server.remark == key)
        else:
            query = query.where(Server.id == key)

        result = await db.execute(query)
        return result.scalar_one_or_none()


async def create_server(remark: str, type: ServerType, data: MarzServerData) -> Server:
    """Create a server in the database."""
    async with get_db() as db:
        server = Server(
            remark=remark,
            type=type,
            data=data,
        )
        db.add(server)
        await db.commit()
        await db.refresh(server)
        return server


async def delete_server(key: Union[str, int]) -> bool:
    """Delete a sepical server with remark or server id"""
    async with get_db() as db:
        query = select(Server)

        if isinstance(key, str):
            query = query.where(Server.remark == key)
        else:
            query = query.where(Server.id == key)

        result = (await db.execute(query)).scalar_one_or_none()

        if result:
            await db.delete(result)
            await db.commit()
            return True

        return False
