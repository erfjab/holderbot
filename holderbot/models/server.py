from pydantic import BaseModel
from enum import Enum


class ServerType(str, Enum):
    """types of servers"""

    MARZBAN = "marzban"
    MARZNESHIN = "marzneshin"


class MarzServerData(BaseModel):
    """data handler for marzban and marzneshin servers"""

    username: str
    password: str
    host: str
