from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class SettingKeys(str, Enum):
    NodeMonitoringIsActive = "node_monitoring_is_active"
    NodeMonitoringAutoRestart = "node_monitoring_auto_restart"


class SettingData(BaseModel):
    key: str
    value: str | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class SettingUpsert(BaseModel):
    key: str
    value: str | None
