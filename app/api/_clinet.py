from typing import Optional

from .clients import MarzneshinApiManager
from .types.marzneshin import MarzneshinToken
from app.models.server import ServerTypes


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
                token = token.access_token if token else None

        return token
