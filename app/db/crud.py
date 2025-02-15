from typing import Optional, Union
from sqlalchemy import select
from .models import (
    Server,
    ServerAccess,
    Template,
)
from .base import get_db
from app.models.server import ServerTypes
from app.models.user import DateTypes


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


async def modify_server(
    serverid: int,
    remark: Optional[str] = None,
    data: Optional[dict] = None,
    node_monitoring: Optional[bool] = None,
    node_restart: Optional[bool] = None,
    expired_stats: Optional[bool] = None,
) -> Optional[Server]:
    async with get_db() as db:
        server = await db.execute(select(Server).filter(Server.id == serverid))
        server = server.scalar_one_or_none()
        if not server:
            return False
        if remark is not None:
            server.remark = remark
        if data is not None:
            server.data = data
        if node_monitoring is not None:
            server.node_monitoring = node_monitoring
        if node_restart is not None:
            server.node_restart = node_restart
        if expired_stats is not None:
            server.expired_stats = expired_stats
        await db.commit()
        await db.refresh(server)
        return server


async def remove_server(serverid: int) -> bool:
    async with get_db() as db:
        server = await db.execute(select(Server).filter(Server.id == serverid))
        server = server.scalar_one_or_none()
        if not server:
            return True
        await db.delete(server.server_access)
        await db.delete(server)
        await db.commit()
        return True


async def get_templates(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    active: Optional[bool] = None,
) -> list[Template]:
    async with get_db() as db:
        query = select(Template)
        if active is not None:
            query = query.where(Template.is_active == active)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        result = await db.execute(query)
        return result.scalars().all()


async def get_template(key: Union[str, int]) -> Optional[Template]:
    async with get_db() as db:
        query = select(Template)

        if isinstance(key, str):
            query = query.where(Template.remark == key)
        else:
            query = query.where(Template.id == key)

        result = await db.execute(query)
        return result.scalar_one_or_none()


async def create_template(
    remark: str,
    data_limit: int,
    date_limit: int,
    date_types: DateTypes,
) -> Template:
    async with get_db() as db:
        template = Template(
            remark=remark,
            data_limit=data_limit,
            date_limit=date_limit,
            date_types=date_types,
        )
        db.add(template)
        await db.commit()
        await db.refresh(template)
        return template


async def modify_template(
    templateid: int,
    remark: Optional[str] = None,
    data_limit: Optional[int] = None,
    date_limit: Optional[int] = None,
    date_types: Optional[DateTypes] = None,
    is_active: Optional[bool] = None,
) -> Template:
    async with get_db() as db:
        template = await db.execute(select(Template).filter(Template.id == templateid))
        template = template.scalar_one_or_none()
        if not template:
            return False
        if remark is not None:
            template.remark = remark
        if data_limit is not None:
            template.data_limit = data_limit
        if date_limit is not None:
            template.date_limit = date_limit
        if date_types is not None:
            template.date_types = date_types
        if is_active is not None:
            template.is_active = is_active
        await db.commit()
        await db.refresh(template)
        return template


async def remove_template(templateid: int) -> bool:
    async with get_db() as db:
        template = await db.execute(select(Template).filter(Template.id == templateid))
        template = template.scalar_one_or_none()
        if not template:
            return True
        await db.delete(template)
        await db.commit()
        return True
