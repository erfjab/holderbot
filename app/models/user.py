from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class MarzneshinUserExpireStrategy(str, Enum):
    NEVER = "never"
    FIXED_DATE = "fixed_date"
    START_ON_FIRST_USE = "start_on_first_use"


class MarzneshinUserCreate(BaseModel):
    username: str
    data_limit: int
    service_ids: List[int]
    expire_strategy: MarzneshinUserExpireStrategy
    expire_date: Optional[str]
    usage_duration: Optional[int]
