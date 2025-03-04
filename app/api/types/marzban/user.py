from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, validator
from .admin import MarzbanAdmin
from app.api.helpers import ensure_utc, format_bytes, format_date_diff


class MarzbanUserDataUsageResetStrategy(str, Enum):
    no_reset = "no_reset"
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class MarzbanUserStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    LIMITED = "limited"
    EXPIRED = "expired"
    ONHOLD = "on_hold"


class MarzbanUserResponse(BaseModel):
    username: Optional[str] = None
    proxies: Optional[Dict[str, dict]] = {}
    expire: Optional[int] = None
    data_limit: Optional[int] = None
    data_limit_reset_strategy: MarzbanUserDataUsageResetStrategy = (
        MarzbanUserDataUsageResetStrategy.no_reset
    )
    inbounds: Optional[Dict[str, List[str]]] = None
    note: Optional[str] = None
    sub_updated_at: Optional[str] = None
    sub_last_user_agent: Optional[str] = None
    online_at: Optional[datetime] = None
    on_hold_expire_duration: Optional[int] = None
    on_hold_timeout: Optional[datetime] = None
    sub_updated_at: Optional[datetime] = None
    status: MarzbanUserStatus = MarzbanUserStatus.ACTIVE
    used_traffic: Optional[int] = None
    lifetime_used_traffic: Optional[int] = None
    links: Optional[List[str]] = []
    subscription_url: Optional[str] = None
    excluded_inbounds: Optional[Dict[str, List[str]]] = None
    admin: Optional[MarzbanAdmin] = None
    created_at: Optional[datetime] = None

    @property
    def remark(self) -> str:
        return self.username

    @property
    def emoji(self) -> str:
        return "✅ " if self.is_active else "❌ "

    @property
    def id(self) -> str:
        return self.username

    @property
    def is_active(self) -> bool:
        return self.status in [MarzbanUserStatus.ACTIVE, MarzbanUserStatus.ONHOLD]

    @property
    def expire_strategy(self) -> str:
        return self.status

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}

    @validator(
        "on_hold_timeout",
        "online_at",
        "sub_updated_at",
        "created_at",
        pre=True,
    )
    def ensure_timezone(cls, v):
        return ensure_utc(v)

    @property
    def is_enable(self) -> bool:
        return self.status in ["active", "on_hold"]

    @property
    def is_limited(self) -> bool:
        return self.status == "limited"

    @property
    def is_expired(self) -> bool:
        return self.status == "expired"

    @property
    def data_percent(self) -> int:
        if not self.data_limit or not self.used_traffic:
            return 100

        if self.used_traffic >= self.data_limit:
            return 0

        return int(((self.data_limit - self.used_traffic) / self.data_limit) * 100)

    @property
    def last_sub_update_hour(self) -> int:
        if not self.sub_updated_at:
            return None
        return int(
            (
                datetime.now(timezone.utc) - ensure_utc(self.sub_updated_at)
            ).total_seconds()
            / 3600
        )

    @property
    def last_online_hour(self) -> int:
        if not self.online_at:
            return None
        return int(
            (datetime.now(timezone.utc) - ensure_utc(self.online_at)).total_seconds()
            / 3600
        )

    @property
    def last_expired_hour(self) -> int:
        if not self.expire:
            return None

        now = datetime.now(timezone.utc)
        refrenc = ensure_utc(datetime.fromtimestamp(self.expire))
        if now >= refrenc:
            return None

        return int((refrenc - now).total_seconds() / 3600)

    @property
    def time_to_second(self) -> int:
        if self.status == "active":
            if self.expire:
                return datetime.fromtimestamp(self.expire).second
        elif self.status == "on_hold":
            if self.on_hold_expire_duration:
                return self.on_hold_expire_duration
        return None

    @property
    def format_data(self) -> dict:
        now = ensure_utc(datetime.now(timezone.utc))

        return {
            "username": self.username,
            "proxies": self.proxies,
            "expire": self.expire,
            "expire_strategy": self.expire_strategy.value,
            "data_limit": format_bytes(self.data_limit) if self.data_limit else None,
            "data_limit_reset_strategy": self.data_limit_reset_strategy,
            "inbounds": self.inbounds,
            "note": self.note,
            "sub_updated_at": format_date_diff(self.sub_updated_at, now)
            if self.sub_updated_at
            else None,
            "sub_last_user_agent": self.sub_last_user_agent,
            "online_at": format_date_diff(self.online_at, now)
            if self.online_at
            else None,
            "on_hold_expire_duration": self.on_hold_expire_duration,
            "on_hold_timeout": format_date_diff(self.on_hold_timeout, now)
            if self.on_hold_timeout
            else None,
            "status": self.status,
            "used_traffic": format_bytes(self.used_traffic)
            if self.used_traffic
            else None,
            "lifetime_used_traffic": format_bytes(self.lifetime_used_traffic)
            if self.lifetime_used_traffic
            else None,
            "subscription_url": self.subscription_url,
            "excluded_inbounds": self.excluded_inbounds,
            "admin": self.admin.dict() if self.admin else None,
            "created_at": format_date_diff(self.created_at, now)
            if self.created_at
            else None,
        }

    def format_data_str(self) -> str:
        """Return formatted data as a string"""
        now = ensure_utc(datetime.now(timezone.utc))

        data = [
            f"<b>• Username:</b> <code>{self.username}</code>",
            f"<b>• Status:</b> <code>{self.status.value}</code>",
            f"<b>• Expire:</b> <code>{format_date_diff(now, datetime.fromtimestamp(self.expire, timezone.utc)) if self.expire else 'Never'}</code>",
            f"<b>• Expire Strategy: </b> <code>{self.expire_strategy.value}</code>",
            f"<b>• Data Limit:</b> <code>{format_bytes(self.data_limit) if self.data_limit else 'Unlimited'}</code>",
            f"<b>• Data Reset Strategy:</b> <code>{self.data_limit_reset_strategy.value}</code>",
            f"<b>• Used Traffic:</b> <code>{format_bytes(self.used_traffic) if self.used_traffic else '0B'}</code>",
            f"<b>• Lifetime Used Traffic:</b> <code>{format_bytes(self.lifetime_used_traffic) if self.lifetime_used_traffic else '0B'}</code>",
            f"<b>• Last Update:</b> <code>{format_date_diff(now, self.sub_updated_at) if self.sub_updated_at else '➖'}</code>",
            f"<b>• Last User Agent:</b> <code>{self.sub_last_user_agent or '➖'}</code>",
            f"<b>• Last Online:</b> <code>{format_date_diff(now, self.online_at) if self.online_at else '➖'}</code>",
            f"<b>• On Hold Expire Duration:</b> <code>{self.on_hold_expire_duration or '➖'}</code>",
            f"<b>• On Hold Timeout:</b> <code>{format_date_diff(now, self.on_hold_timeout) if self.on_hold_timeout else '➖'}</code>",
            f"<b>• Note:</b> <code>{self.note or '➖'}</code>",
            f"<b>• Subscription URL:</b> <code>{self.subscription_url or '➖'}</code>",
            f"<b>• Created At:</b> <code>{format_date_diff(now, self.created_at) if self.created_at else '➖'}</code>",
            f"<b>• Admin:</b> <code>{self.admin.username if self.admin else '➖'}</code>",
        ]

        return "\n".join(data)
