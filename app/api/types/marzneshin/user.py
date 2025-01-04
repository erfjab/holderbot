from datetime import datetime
from pydantic import BaseModel


class MarzneshinUserResponse(BaseModel):
    id: int
    username: str
    activated: bool
    is_active: bool
    expired: bool
    data_limit_reached: bool
    enabled: bool
    used_traffic: int
    lifetime_used_traffic: int
    sub_revoked_at: datetime | None
    created_at: datetime
    service_ids: list[int]
    subscription_url: str
    owner_username: str | None
    traffic_reset_at: datetime | None

    @property
    def remark(self):
        return self.username

    @property
    def emoji(self):
        return "✅ " if self.is_active else "❌ "
