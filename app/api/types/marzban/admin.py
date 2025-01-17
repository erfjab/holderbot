from typing import Optional
from pydantic import BaseModel


class MarzbanToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MarzbanAdmin(BaseModel):
    username: str
    is_sudo: bool
    telegram_id: Optional[int] = None
    discord_webhook: Optional[str] = None
    users_usage: Optional[int] = None
