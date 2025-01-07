from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class MarzneshinUserExpireStrategy(str, Enum):
    NEVER = "never"
    FIXED_DATE = "fixed_date"
    START_ON_FIRST_USE = "start_on_first_use"


class MarzneshinUserCreate(BaseModel):
    username: str
    data_limit: int
    service_ids: list[int]
    expire_strategy: MarzneshinUserExpireStrategy
    expire_date: datetime | None
    usage_duration: int | None


class UserModify(str, Enum):
    ACTIVATED = "Activated"
    DISABLED = "Disabled"
    REVOKE = "Revoke"
    RESET_USAGE = "Reset usage"
    QRCODE = "Qrcode"
    REMOVE = "Remove"
