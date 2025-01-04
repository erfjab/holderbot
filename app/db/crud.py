from typing import Optional, Union
from sqlalchemy import select
from .models import (
    Server,
    ServerAccess,
)
from .base import get_db
from app.models.server import ServerTypes


async def upsert_server_access(serverid: int, serveraccess: str):
    async with get_db() as db:
        access = await db.execute(
            select(ServerAccess).where(ServerAccess.server_id == serverid)
        )
        access = access.scalar_one_or_none()

        if access:
            access.access = serveraccess
        else:
            access = ServerAccess(access=serveraccess, server_id=serverid)
            db.add(access)

        await db.commit()
        await db.refresh(access)
        return access


async def get_servers(
    types: Optional[ServerTypes] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    active: Optional[bool] = None,
) -> list[Server]:
    async with get_db() as db:
        query = select(Server)
        if active is not None:
            query = query.where(Server.is_active == active)
        if types:
            query = query.where(Server.types == types)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        result = await db.execute(query)
        return result.scalars().all()


async def get_server(key: Union[str, int]) -> Optional[Server]:
    async with get_db() as db:
        query = select(Server)

        if isinstance(key, str):
            query = query.where(Server.remark == key)
        else:
            query = query.where(Server.id == key)

        result = await db.execute(query)
        return result.scalar_one_or_none()


async def create_server(
    remark: str,
    types: ServerTypes,
    data: dict,
) -> Server:
    async with get_db() as db:
        server = Server(
            remark=remark,
            types=types,
            data=data,
        )
        db.add(server)
        await db.commit()
        await db.refresh(server)
        return server
