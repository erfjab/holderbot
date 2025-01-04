from enum import Enum
from pydantic import BaseModel


class ServerTypes(str, Enum):
    MARZNESHIN = "marzneshin"


class MarzneshinServerData(BaseModel):
    username: str
    password: str
    host: str


class ServerModify(str, Enum):
    STATUS = "status"
    REMARK = "remark"
    DATA = "data"
