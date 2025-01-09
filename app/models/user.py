from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class MarzneshinUserExpireStrategy(str, Enum):
    NEVER = "never"
    FIXED_DATE = "fixed_date"
    START_ON_FIRST_USE = "start_on_first_use"


class DateTypes(str, Enum):
    UNLIMITED = "unlimited"
    NOW = "now"
    AFTER_FIRST_USE = "after first use"


class MarzneshinUserCreate(BaseModel):
    username: str
    data_limit: int
    service_ids: list[int]
    expire_strategy: MarzneshinUserExpireStrategy
    expire_date: datetime | None
    usage_duration: int | None


class MarzneshinUserModify(BaseModel):
    username: str
    data_limit: int | None = None
    service_ids: list[int] | None = None
    expire_strategy: MarzneshinUserExpireStrategy | None = None
    expire_date: datetime | None = None
    usage_duration: int | None = None


class UserModify(str, Enum):
    ACTIVATED = "✅ Activated"
    DISABLED = "❌ Disabled"
    REVOKE = "⛓️‍💥 Revoke"
    RESET_USAGE = "🔁 Reset usage"
    QRCODE = "🖼 Qrcode"
    REMOVE = "🗑 Remove"
    OWNER = "👤 Set owner"
    CONFIGS = "📂 Configs"
    DATA_LIMIT = "📊 Data Limit"
    DATE_LIMIT = "⏱️ Date Limit"
