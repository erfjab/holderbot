from typing import Optional

from ..core import ApiRequest
from ..types.marzneshin import (
    MarzneshinToken,
    MarzneshinUserResponse,
    MarzneshinServiceResponce,
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
        self, access: str, page: Optional[int] = None, size: Optional[int] = None
    ) -> Optional[list[MarzneshinUserResponse]]:
        users = await self.get(
            endpoint="/api/users", params={"page": page, "size": size}, access=access
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
