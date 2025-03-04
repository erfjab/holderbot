from typing import Optional

from ..core import ApiRequest
from ..types.marzneshin import (
    MarzneshinToken,
    MarzneshinUserResponse,
    MarzneshinServiceResponce,
    MarzneshinAdmin,
    MarzneshinNodeResponse,
)


class MarzneshinApiManager(ApiRequest):
    async def get_token(
        self, username: str, password: str
    ) -> Optional[MarzneshinToken]:
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        return await self.post(
            endpoint="/api/admins/token",
            data=data,
            response_model=MarzneshinToken,
        )

    async def get_users(
        self,
        access: str,
        page: Optional[int] = None,
        size: Optional[int] = None,
        expired: Optional[bool] = None,
        limited: Optional[bool] = None,
        search: Optional[str] = None,
        owner_username: Optional[str] = None,
        is_active: Optional[str] = None,
    ) -> Optional[list[MarzneshinUserResponse]]:
        users = await self.get(
            endpoint="/api/users",
            params={
                "page": page,
                "size": size,
                "order_by": "created_at",
                "descending": True,
                "expired": expired,
                "data_limit_reached": limited,
                "username": search,
                "owner_username": owner_username,
                "is_active": is_active,
            },
            access=access,
        )
        if not users:
            return False
        return [MarzneshinUserResponse(**user) for user in users["items"]]

    async def get_user(
        self, username: str, access: str
    ) -> Optional[MarzneshinUserResponse]:
        return await self.get(
            endpoint=f"/api/users/{username}",
            access=access,
            response_model=MarzneshinUserResponse,
        )

    async def modify_user(
        self, username: str, data: dict, access: str
    ) -> Optional[MarzneshinUserResponse]:
        return await self.put(
            endpoint=f"/api/users/{username}",
            access=access,
            data=data,
            response_model=MarzneshinUserResponse,
        )

    async def get_services(
        self, access: str
    ) -> Optional[list[MarzneshinServiceResponce]]:
        services = await self.get(endpoint="/api/services", access=access)
        if not services:
            return False
        return [MarzneshinServiceResponce(**service) for service in services["items"]]

    async def create_user(
        self, data: dict, access: str
    ) -> Optional[MarzneshinUserResponse]:
        return await self.post(
            endpoint="/api/users",
            access=access,
            data=data,
            response_model=MarzneshinUserResponse,
        )

    async def remove_user(self, username: str, access: str) -> bool:
        return await self.delete(
            endpoint=f"/api/users/{username}",
            access=access,
        )

    async def activate_user(self, username: str, access: str) -> bool:
        return await self.post(endpoint=f"/api/users/{username}/enable", access=access)

    async def disabled_user(self, username: str, access: str) -> bool:
        return await self.post(endpoint=f"/api/users/{username}/disable", access=access)

    async def activate_users(self, admin: str, access: str) -> bool:
        return await self.post(
            endpoint=f"/api/admins/{admin}/enable_users", access=access
        )

    async def disabled_users(self, admin: str, access: str) -> bool:
        return await self.post(
            endpoint=f"/api/admins/{admin}/disable_users", access=access
        )

    async def revoke_user(self, username: str, access: str) -> bool:
        return await self.post(
            endpoint=f"/api/users/{username}/revoke_sub",
            access=access,
            response_model=MarzneshinUserResponse,
        )

    async def reset_user(self, username: str, access: str) -> bool:
        return await self.post(endpoint=f"/api/users/{username}/reset", access=access)

    async def get_admins(self, access: str) -> Optional[list[MarzneshinAdmin]]:
        admins = await self.get(endpoint="/api/admins", access=access)
        if not admins:
            return False
        return [MarzneshinAdmin(**admin) for admin in admins["items"]]

    async def set_owner(self, username: str, admin: str, access: str) -> bool:
        return await self.put(
            endpoint=f"/api/users/{username}/set-owner",
            params={"username": username, "admin_username": admin},
            access=access,
        )

    async def get_nodes(self, access: str) -> Optional[MarzneshinNodeResponse]:
        nodes = await self.get(endpoint="/api/nodes", access=access)
        if not nodes:
            return False
        return [MarzneshinNodeResponse(**node) for node in nodes["items"]]

    async def restart_node(self, access: str, nodeid: int) -> bool:
        return await self.post(endpoint=f"/api/nodes/{nodeid}/resync", access=access)
