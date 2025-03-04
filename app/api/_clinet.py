from typing import Optional

from .clients import MarzneshinApiManager, MarzbanApiManager
from .types.marzneshin import (
    MarzneshinToken,
    MarzneshinUserResponse,
    MarzneshinServiceResponce,
    MarzneshinAdmin,
    MarzneshinNodeResponse,
)
from .types.marzban import (
    MarzbanAdmin,
    MarzbanProxyInbound,
    MarzbanToken,
    MarzbanUserResponse,
    MarzbanUserStatus,
    MarzbanNodeResponse,
)
from app.models.server import ServerTypes
from app.db import Server


class ClinetApiManager:
    async def generate_access(
        self,
        data: Optional[dict],
        types: Optional[ServerTypes],
    ) -> Optional[MarzneshinToken | MarzbanToken]:
        match types:
            case ServerTypes.MARZNESHIN:
                api = MarzneshinApiManager(host=data["host"])
                token = await api.get_token(data["username"], data["password"])
                token = token.access_token if token and token.is_sudo is True else False

            case ServerTypes.MARZBAN:
                api = MarzbanApiManager(host=data["host"])
                token = await api.get_token(data["username"], data["password"])
                if token:
                    admin = await api.get_admin(access=token.access_token)
                    token = token.access_token if admin.is_sudo else False

        return token

    async def get_users(
        self,
        server: Server,
        page: Optional[int] = 1,
        size: Optional[int] = 10,
        limited: Optional[bool] = None,
        expired: Optional[bool] = None,
        search: Optional[str] = None,
        owner_username: Optional[str] = None,
        is_active: Optional[str] = None,
    ) -> Optional[list[MarzneshinUserResponse] | list[MarzbanUserResponse]]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                users = await api.get_users(
                    access=server.access,
                    page=page,
                    size=size,
                    expired=expired,
                    limited=limited,
                    search=search,
                    owner_username=owner_username,
                    is_active=is_active,
                )

            case ServerTypes.MARZBAN.value:
                status = None
                if expired:
                    status = MarzbanUserStatus.EXPIRED.value
                if limited:
                    status = MarzbanUserStatus.LIMITED.value
                if is_active:
                    status = MarzbanUserStatus.ACTIVE.value
                api = MarzbanApiManager(host=server.data["host"])
                users = await api.get_users(
                    access=server.access,
                    offset=((page - 1) * size),
                    limit=size,
                    status=status,
                    search=search,
                    owner_username=owner_username,
                )
        return users

    async def get_user(
        self, server: Server, username: str
    ) -> Optional[MarzneshinUserResponse | MarzbanUserResponse]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                user = await api.get_user(username=username, access=server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                user = await api.get_user(username=username, access=server.access)

        return user

    async def get_configs(
        self, server: Server
    ) -> Optional[MarzneshinServiceResponce | MarzbanProxyInbound]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                configs = await api.get_services(access=server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                configs = await api.get_inbounds(access=server.access)

        return configs

    async def create_user(
        self, server: Server, data: dict
    ) -> Optional[MarzneshinUserResponse | MarzbanUserResponse]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                user = await api.create_user(data, server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                user = await api.create_user(data, server.access)

        return user

    async def modify_user(
        self, server: Server, username: str, data: dict
    ) -> Optional[MarzneshinUserResponse | MarzbanUserResponse]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                user = await api.modify_user(username, data, server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                user = await api.modify_user(username, data, server.access)

        return user

    async def remove_user(self, server: Server, username: str) -> bool:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                user = await api.remove_user(username, server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                user = await api.remove_user(username, server.access)

        return user

    async def activated_user(self, server: Server, username: str) -> bool:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                user = await api.activate_user(username, server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                user = await api.activate_user(username, server.access)

        return user

    async def disabled_user(self, server: Server, username: str) -> bool:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                user = await api.disabled_user(username, server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                user = await api.disabled_user(username, server.access)

        return user

    async def reset_user(self, server: Server, username: str) -> bool:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                user = await api.reset_user(username, server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                user = await api.reset_user(username, server.access)

        return user

    async def revoke_user(
        self, server: Server, username: str
    ) -> Optional[MarzneshinUserResponse | MarzbanUserResponse]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                user = await api.revoke_user(username, server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                user = await api.revoke_user(username, server.access)

        return user

    async def get_admins(
        self, server: Server
    ) -> Optional[list[MarzneshinAdmin] | list[MarzbanAdmin]]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                admins = await api.get_admins(access=server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                admins = await api.get_admins(access=server.access)

        return admins

    async def set_owner(
        self, server: Server, username: str, admin: str
    ) -> Optional[MarzneshinUserResponse]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                user = await api.set_owner(
                    username=username, admin=admin, access=server.access
                )

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                user = await api.set_owner(
                    username=username, admin=admin, access=server.access
                )

        return user

    async def activated_users(self, server: Server, admin: str) -> bool:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                action = await api.activate_users(admin, server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                action = await api.activate_users(admin, server.access)

        return action

    async def disabled_users(self, server: Server, admin: str) -> bool:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                action = await api.disabled_users(admin, server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                action = await api.disabled_users(admin, server.access)

        return action

    async def get_nodes(
        self, server: Server
    ) -> Optional[list[MarzneshinNodeResponse] | list[MarzbanNodeResponse]]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                nodes = await api.get_nodes(server.access)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                nodes = await api.get_nodes(server.access)

        return nodes

    async def restart_node(self, server: Server, nodeid: int) -> bool:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                action = await api.restart_node(server.access, nodeid)

            case ServerTypes.MARZBAN.value:
                api = MarzbanApiManager(host=server.data["host"])
                action = await api.restart_node(server.access, nodeid)

        return action
