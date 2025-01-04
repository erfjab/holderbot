from typing import Optional

from .clients import MarzneshinApiManager
from .types.marzneshin import (
    MarzneshinToken,
    MarzneshinUserResponse,
    MarzneshinServiceResponce,
)
from app.models.server import ServerTypes
from app.db import Server


class ClinetApiManager:
    async def generate_access(
        self,
        data: Optional[dict],
        types: Optional[ServerTypes],
    ) -> Optional[MarzneshinToken]:
        match types:
            case ServerTypes.MARZNESHIN:
                api = MarzneshinApiManager(host=data["host"])
                token = await api.get_token(data["username"], data["password"])
                token = token.access_token if token and token.is_sudo is True else None

        return token

    async def get_users(
        self,
        server: Server,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> Optional[list[MarzneshinUserResponse]]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                users = await api.get_users(access=server.access, page=page, size=size)

        return users

    async def get_user(
        self, server: Server, username: str
    ) -> Optional[MarzneshinUserResponse]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                user = await api.get_user(username=username, access=server.access)

        return user

    async def get_configs(self, server: Server) -> Optional[MarzneshinServiceResponce]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                configs = await api.get_services(access=server.access)

        return configs

    async def create_user(
        self, server: Server, data: dict
    ) -> Optional[MarzneshinUserResponse]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                api = MarzneshinApiManager(host=server.data["host"])
                user = await api.create_user(data, server.access)

        return user
