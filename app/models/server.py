from enum import Enum
from pydantic import BaseModel


class ServerTypes(str, Enum):
    MARZNESHIN = "marzneshin"


class MarzneshinServerData(BaseModel):
    username: str
    password: str
    host: str


class ServerModify(str, Enum):
    REMARK = "remark"
    DATA = "data"
    REMOVE = "remove"
