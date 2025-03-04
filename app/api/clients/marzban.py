from typing import Optional

from ..core import ApiRequest
from ..types.marzban import (
    MarzbanToken,
    MarzbanAdmin,
    MarzbanUserResponse,
    MarzbanProxyInbound,
    MarzbanUserStatus,
    MarzbanNodeResponse,
)


class MarzbanApiManager(ApiRequest):
    async def get_token(self, username: str, password: str) -> Optional[MarzbanToken]:
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        return await self.post(
            endpoint="/api/admin/token",
            data=data,
            response_model=MarzbanToken,
        )

    async def get_admin(
        self, access: str, username: Optional[str] = None
    ) -> Optional[MarzbanAdmin]:
        return await self.get(
            endpoint=f"/api/admin/{username}" if username else "/api/admin",
            access=access,
            response_model=MarzbanAdmin,
        )

    async def get_users(
        self,
        access: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        status: Optional[MarzbanUserStatus] = None,
        search: Optional[str] = None,
        owner_username: Optional[str] = None,
    ) -> Optional[list[MarzbanUserResponse]]:
        users = await self.get(
            endpoint="/api/users",
            params={
                "offset": offset,
                "limit": limit,
                "sort": "-created_at",
                "status": status,
                "search": search,
                "admin": owner_username,
            },
            access=access,
        )
        if not users:
            return False
        return [MarzbanUserResponse(**user) for user in users["users"]]

    async def get_user(
        self, username: str, access: str
    ) -> Optional[MarzbanUserResponse]:
        return await self.get(
            endpoint=f"/api/user/{username}",
            access=access,
            response_model=MarzbanUserResponse,
        )

    async def modify_user(
        self, username: str, data: dict, access: str
    ) -> Optional[MarzbanUserResponse]:
        return await self.put(
            endpoint=f"/api/user/{username}",
            access=access,
            data=data,
            response_model=MarzbanUserResponse,
        )

    async def get_inbounds(self, access: str) -> Optional[list[MarzbanProxyInbound]]:
        inbounds: dict = await self.get(endpoint="/api/inbounds", access=access)
        if not inbounds:
            return None
        return [
            MarzbanProxyInbound(**inbound)
            for inbound_list in inbounds.values()
            for inbound in (
                inbound_list if isinstance(inbound_list, list) else [inbound_list]
            )
        ]

    async def create_user(
        self, data: dict, access: str
    ) -> Optional[MarzbanUserResponse]:
        return await self.post(
            endpoint="/api/user",
            access=access,
            data=data,
            response_model=MarzbanUserResponse,
        )

    async def remove_user(self, username: str, access: str) -> bool:
        return await self.delete(
            endpoint=f"/api/user/{username}",
            access=access,
        )

    async def activate_user(self, username: str, access: str) -> bool:
        return await self.put(
            endpoint=f"/api/user/{username}", data={"status": "active"}, access=access
        )

    async def disabled_user(self, username: str, access: str) -> bool:
        return await self.put(
            endpoint=f"/api/user/{username}", data={"status": "disabled"}, access=access
        )

    async def activate_users(self, admin: str, access: str) -> bool:
        return await self.post(
            endpoint=f"/api/admin/{admin}/users/activate", access=access
        )

    async def disabled_users(self, admin: str, access: str) -> bool:
        return await self.post(
            endpoint=f"/api/admin/{admin}/users/disable", access=access
        )

    async def revoke_user(self, username: str, access: str) -> bool:
        return await self.post(
            endpoint=f"/api/user/{username}/revoke_sub",
            access=access,
            response_model=MarzbanUserResponse,
        )

    async def reset_user(self, username: str, access: str) -> bool:
        return await self.post(endpoint=f"/api/user/{username}/reset", access=access)

    async def get_admins(self, access: str) -> Optional[list[MarzbanAdmin]]:
        admins = await self.get(endpoint="/api/admins", access=access)
        if not admins:
            return False
        return [MarzbanAdmin(**admin) for admin in admins]

    async def set_owner(self, username: str, admin: str, access: str) -> bool:
        return await self.put(
            endpoint=f"/api/user/{username}/set-owner",
            params={"username": username, "admin_username": admin},
            access=access,
        )

    async def get_nodes(self, access: str) -> Optional[MarzbanNodeResponse]:
        nodes = await self.get(endpoint="/api/nodes", access=access)
        if not nodes:
            return False
        return [MarzbanNodeResponse(**node) for node in nodes]

    async def restart_node(self, access: str, nodeid: int) -> bool:
        return await self.post(endpoint=f"/api/node/{nodeid}/reconnect", access=access)
