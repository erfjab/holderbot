from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, validator
from typing import Optional
from app.api.helpers import format_bytes, format_date_diff, ensure_utc


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
                usage_duration = self.usage_duration / (24 * 60 * 60)
                return f"{int(usage_duration)} days after first use"
            return "Unknown"
        return "Unknown"

    @property
    def is_enable(self) -> bool:
        return self.activated

    @property
    def is_limited(self) -> bool:
        return self.data_limit_reached

    @property
    def is_expired(self) -> bool:
        return self.expired

    @property
    def time_to_second(self) -> int:
        if self.expire_strategy == UserExpireStrategy.NEVER:
            return 0
        elif self.expire_strategy == UserExpireStrategy.FIXED_DATE and self.expire_date:
            return int(
                (
                    self.expire_date.astimezone(timezone.utc)
                    - datetime.now(timezone.utc)
                ).total_seconds()
            )
        elif (
            self.expire_strategy == UserExpireStrategy.START_ON_FIRST_USE
            and self.usage_duration
        ):
            return self.usage_duration
        return 0

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
        if (
            self.expire_strategy
            in [UserExpireStrategy.NEVER, UserExpireStrategy.START_ON_FIRST_USE]
            or not self.expire_date
        ):
            return None

        now = datetime.now(timezone.utc)
        refrenc = ensure_utc(self.expire_date)
        if now >= refrenc:
            return None

        return int((refrenc - now).total_seconds() / 3600)

    @property
    def format_data(self) -> dict:
        now = ensure_utc(datetime.now(timezone.utc))

        return {
            "username": self.username,
            "expire_strategy": f"{self.expire_strategy.value} ({self.get_expire_info(now)})",
            "activation_deadline": format_date_diff(now, self.activation_deadline),
            "data_limit": format_bytes(self.data_limit)
            if self.data_limit
            else "Unlimited",
            "data_reset_strategy": self.data_limit_reset_strategy.value,
            "used_traffic": format_bytes(self.used_traffic),
            "total_used_traffic": format_bytes(self.lifetime_used_traffic),
            "last_update": format_date_diff(now, self.sub_updated_at),
            "last_user_agent": self.sub_last_user_agent or "➖",
            "last_online": format_date_diff(now, self.online_at),
            "is_activated": "Yes" if self.activated else "No",
            "is_enabled": "Yes" if self.enabled else "No",
            "is_active": "Yes" if self.is_active else "No",
            "is_expired": "Yes" if self.expired else "No",
            "data_limit_reached": "Yes" if self.data_limit_reached else "No",
            "services": str(self.service_ids),
            "owner": self.owner_username or "➖",
            "note": self.note or "➖",
            "revoked_at": format_date_diff(now, self.sub_revoked_at),
            "traffic_reset_at": format_date_diff(now, self.traffic_reset_at),
            "created_at": format_date_diff(now, self.created_at),
            "subscription_url": self.subscription_url,
        }

    def format_data_str(self) -> str:
        """Return formatted data as a string"""
        now = ensure_utc(datetime.now(timezone.utc))

        data = [
            f"<b>• Username:</b> <code>{self.username}</code>",
            f"<b>• Expire Strategy:</b> <code>{self.expire_strategy.value} ({self.get_expire_info(now)})</code>",
            f"<b>• Activation Deadline:</b> <code>{format_date_diff(now, self.activation_deadline)}</code>",
            f"<b>• Data Limit:</b> <code>{format_bytes(self.data_limit) if self.data_limit else 'Unlimited'}</code>",
            f"<b>• Data Reset Strategy:</b> <code>{self.data_limit_reset_strategy.value}</code>",
            f"<b>• Used Traffic:</b> <code>{format_bytes(self.used_traffic)}</code>",
            f"<b>• Total Used Traffic:</b> <code>{format_bytes(self.lifetime_used_traffic)}</code>",
            f"<b>• Last Update:</b> <code>{format_date_diff(now, self.sub_updated_at)}</code>",
            f"<b>• Last User Agent:</b> <code>{self.sub_last_user_agent or '➖'}</code>",
            f"<b>• Last Online:</b> <code>{format_date_diff(now, self.online_at)}</code>",
            f"<b>• Activated:</b> <code>{'Yes' if self.activated else 'No'}</code>",
            f"<b>• Enabled:</b> <code>{'Yes' if self.enabled else 'No'}</code>",
            f"<b>• Active:</b> <code>{'Yes' if self.is_active else 'No'}</code>",
            f"<b>• Expired:</b> <code>{'Yes' if self.expired else 'No'}</code>",
            f"<b>• Data Limit Reached:</b> <code>{'Yes' if self.data_limit_reached else 'No'}</code>",
            f"<b>• Services:</b> <code>{', '.join(map(str, self.service_ids))}</code>",
            f"<b>• Owner:</b> <code>{self.owner_username or '➖'}</code>",
            f"<b>• Note:</b> <code>{self.note or '➖'}</code>",
            f"<b>• Revoked At:</b> <code>{format_date_diff(now, self.sub_revoked_at)}</code>",
            f"<b>• Traffic Reset At:</b> <code>{format_date_diff(now, self.traffic_reset_at)}</code>",
            f"<b>• Created At:</b> <code>{format_date_diff(now, self.created_at)}</code>",
            f"<b>• Subscription URL:</b> <code>{self.subscription_url}</code>",
        ]

        return "\n".join(data)
