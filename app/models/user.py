from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class MarzbanUserStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    LIMITED = "limited"
    EXPIRED = "expired"
    ONHOLD = "on_hold"


class MarzneshinUserExpireStrategy(str, Enum):
    NEVER = "never"
    FIXED_DATE = "fixed_date"
    START_ON_FIRST_USE = "start_on_first_use"


class DateTypes(str, Enum):
    UNLIMITED = "unlimited"
    NOW = "now"
    AFTER_FIRST_USE = "after first use"


class UserJsonData(BaseModel):
    username: str
    datalimit: str | int
    datelimit: str | int
    datetypes: DateTypes

    def to_dict(self):
        return {
            "username": self.username,
            "datalimit": self.datalimit,
            "datelimit": self.datelimit,
            "datetypes": self.datetypes,
        }


class MarzneshinUserCreate(BaseModel):
    username: str
    data_limit: int
    service_ids: list[int]
    expire_strategy: MarzneshinUserExpireStrategy
    expire_date: datetime | None
    usage_duration: int | None


class MarzbanUserCreate(BaseModel):
    username: str
    data_limit: int
    inbounds: dict
    proxies: dict
    status: MarzbanUserStatus
    expire: int | None = None
    on_hold_expire_duration: int | None = None


class MarzbanUserModify(BaseModel):
    data_limit: int | None = None
    inbounds: dict | None = None
    proxies: dict | None = None
    status: MarzbanUserStatus | None = None
    expire: int | None = None
    on_hold_expire_duration: int | None = None
    note: str | None = None


class MarzneshinUserModify(BaseModel):
    username: str
    data_limit: int | None = None
    service_ids: list[int] | None = None
    expire_strategy: MarzneshinUserExpireStrategy | None = None
    expire_date: datetime | None = None
    usage_duration: int | None = None
    note: str | None = None


class UserModify(str, Enum):
    ACTIVATED = "✅ Activated"
    DISABLED = "❌ Disabled"
    REVOKE = "⛓️‍💥 Revoke"
    RESET_USAGE = "🔁 Reset Usage"
    QRCODE = "🖼 Qrcode"
    REMOVE = "🗑 Remove"
    OWNER = "👤 Set Owner"
    CONFIGS = "📂 Configs"
    DATA_LIMIT = "📊 Data Limit"
    DATE_LIMIT = "⏱️ Date Limit"
    NOTE = "🗒 Note"
    CHARGE = "🧪 Charge"
