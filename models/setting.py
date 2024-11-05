"""
Module defining settings models for application configuration.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SettingKeys(str, Enum):
    """Enum for application setting keys."""

    NODE_MONITORING_IS_ACTIVE = "node_monitoring_is_active"
    NODE_MONITORING_AUTO_RESTART = "node_monitoring_auto_restart"


class SettingData(BaseModel):
    """Model for application setting data."""

    key: str
    value: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    # pylint: disable=R0903
    class Config:
        """Pydantic configuration options."""

        from_attributes = True


class SettingUpsert(BaseModel):
    """Model for upserting a setting."""

    key: str
    value: Optional[str]
