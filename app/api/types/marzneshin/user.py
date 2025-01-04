from datetime import datetime, timezone, timedelta
from enum import Enum
from pydantic import BaseModel, validator
from typing import Optional


class UserDataUsageResetStrategy(str, Enum):
    no_reset = "no_reset"
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class UserExpireStrategy(str, Enum):
    NEVER = "never"
    FIXED_DATE = "fixed_date"
    START_ON_FIRST_USE = "start_on_first_use"


def ensure_utc(dt: Optional[datetime | str]) -> Optional[datetime]:
    """Ensure datetime is UTC timezone-aware"""
    if dt is None:
        return None

    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except ValueError:
            try:
                dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(f"Unable to parse datetime string: {dt}")

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def format_bytes(bytes: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ["bytes", "KB", "MB", "GB", "TB"]:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"


def format_date_diff(reference_date: datetime, date: Optional[datetime]) -> str:
    """Calculate time difference between dates"""
    if not date:
        return "➖"

    ref_date = ensure_utc(reference_date)
    compare_date = ensure_utc(date)

    diff = compare_date - ref_date
    total_seconds = int(diff.total_seconds())

    if total_seconds == 0:
        return "now"

    abs_seconds = abs(total_seconds)

    if abs_seconds < 60:
        result = f"{abs_seconds} sec"
    elif abs_seconds < 3600:
        result = f"{abs_seconds // 60} min"
    elif abs_seconds < 86400:
        result = f"{abs_seconds // 3600} hour"
    else:
        result = f"{abs(diff.days)} day"

    return f"in {result}" if total_seconds > 0 else f"{result} ago"


class MarzneshinUserResponse(BaseModel):
    username: str
    expire_strategy: UserExpireStrategy
    expire_date: Optional[datetime]
    usage_duration: Optional[int]
    activation_deadline: Optional[datetime]
    key: Optional[str]
    data_limit: Optional[int]
    data_limit_reset_strategy: UserDataUsageResetStrategy
    note: Optional[str]
    sub_updated_at: Optional[datetime]
    sub_last_user_agent: Optional[str]
    online_at: Optional[datetime]
    activated: bool
    is_active: bool
    expired: bool
    data_limit_reached: bool
    enabled: bool
    used_traffic: int
    lifetime_used_traffic: int
    sub_revoked_at: Optional[datetime]
    created_at: datetime
    service_ids: list[int]
    subscription_url: str
    owner_username: Optional[str]
    traffic_reset_at: Optional[datetime]

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}

    # Validator for all datetime fields
    @validator(
        "expire_date",
        "activation_deadline",
        "sub_updated_at",
        "online_at",
        "sub_revoked_at",
        "created_at",
        "traffic_reset_at",
        pre=True,
    )
    def ensure_timezone(cls, v):
        return ensure_utc(v)

    @property
    def remark(self) -> str:
        return self.username

    @property
    def emoji(self) -> str:
        return "✅ " if self.is_active else "❌ "

    @property
    def id(self) -> str:
        return self.username

    def get_expire_info(self, now: datetime) -> str:
        now = ensure_utc(now)
        if self.expire_strategy == UserExpireStrategy.NEVER:
            return "Never expires"
        elif self.expire_strategy == UserExpireStrategy.FIXED_DATE and self.expire_date:
            return format_date_diff(now, self.expire_date)
        elif self.expire_strategy == UserExpireStrategy.START_ON_FIRST_USE:
            if self.usage_duration:
                if not self.activated:
                    return f"{self.usage_duration} days after first use"
                else:
                    activation_date = ensure_utc(self.online_at or self.created_at)
                    expire_date = activation_date + timedelta(days=self.usage_duration)
                    return format_date_diff(now, expire_date)
            return "Unknown"
        return "Unknown"

    @property
    def format_data(self) -> str:
        now = ensure_utc(datetime.now(timezone.utc))

        base_data = {
            "Username": self.username,
            "Expire Strategy": f"{self.expire_strategy.value} ({self.get_expire_info(now)})",
            "Activation Deadline": format_date_diff(now, self.activation_deadline),
            "Data Limit": format_bytes(self.data_limit)
            if self.data_limit
            else "Unlimited",
            "Data Reset Strategy": self.data_limit_reset_strategy.value,
            "Used Traffic": format_bytes(self.used_traffic),
            "Total Used Traffic": format_bytes(self.lifetime_used_traffic),
            "Last Update": format_date_diff(now, self.sub_updated_at),
            "Last User Agent": self.sub_last_user_agent or "➖",
            "Last Online": format_date_diff(now, self.online_at),
            "Activated": "Yes" if self.activated else "No",
            "Enabled": "Yes" if self.enabled else "No",
            "Active": "Yes" if self.is_active else "No",
            "Expired": "Yes" if self.expired else "No",
            "Data Limit Reached": "Yes" if self.data_limit_reached else "No",
            "Services": str(self.service_ids),
            "Owner": self.owner_username or "➖",
            "Note": self.note or "➖",
        }

        formatted_data_str = "\n".join(
            [
                f"     • <b>{key}:</b> <code>{value}</code>"
                for key, value in base_data.items()
            ]
        )

        footer_data = [
            f"• <b>Subscription Revoked At:</b> <code>{format_date_diff(now, self.sub_revoked_at)}</code>",
            f"• <b>Traffic Reset At:</b> <code>{format_date_diff(now, self.traffic_reset_at)}</code>",
            f"• <b>Created At:</b> <code>{format_date_diff(now, self.created_at)}</code>",
        ]

        return f"• <b>Data</b>\n{formatted_data_str}\n" + "\n".join(footer_data)
