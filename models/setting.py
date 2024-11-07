"""
Module defining settings models for application configuration.
"""

from enum import Enum


class SettingKeys(Enum):
    """Enum for settings table columns."""

    NODE_MONITORING = "node_monitoring"
    NODE_AUTO_RESTART = "node_auto_restart"
