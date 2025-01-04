from typing import Optional

from .clients import MarzneshinApiManager
from .types.marzneshin import MarzneshinToken, MarzneshinUserResponse
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
                marzbanapi = MarzneshinApiManager(host=data["host"])
                token = await marzbanapi.get_token(data["username"], data["password"])
                token = token.access_token if token and token.is_sudo is True else None

        return token

    async def get_users(
        self,
        server: Server,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> Optional[MarzneshinUserResponse]:
        match server.types:
            case ServerTypes.MARZNESHIN.value:
                marzbanapi = MarzneshinApiManager(host=server.data["host"])
                users = await marzbanapi.get_users(
                    access=server.access, page=page, size=size
                )

        return users
