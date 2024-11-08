"""
This module provides functionality for managing application settings,
including methods for updating and retrieving settings.
"""

from typing import List

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from db.models import Setting
from models import SettingKeys


class SettingManager:
    """Handles the application's settings management, ensuring a single settings record exists."""

    @staticmethod
    async def _get_or_create_settings(db: AsyncSession) -> Setting:
        """
        Helper method to get existing settings or create new ones if they don't exist.
        """
        result = await db.execute(select(Setting))
        settings = result.scalar_one_or_none()

        if not settings:
            settings = Setting()
            db.add(settings)
            await db.commit()
            await db.refresh(settings)

        return settings

    @staticmethod
    async def get(field: SettingKeys) -> bool:
        """
        Retrieve the specified setting field, ensuring the settings record exists.
        If the settings record does not exist, it will be created.
        """
        async with get_db() as db:
            settings = await SettingManager._get_or_create_settings(db)
            return getattr(settings, field.value)

    @staticmethod
    async def toggle_field(field: SettingKeys) -> bool:
        """
        Toggle a boolean setting field and return its new value.
        Ensures the settings record exists before toggling.
        """
        async with get_db() as db:
            settings = await SettingManager._get_or_create_settings(db)

            # Toggle the field's current value
            current_value = getattr(settings, field.value)
            new_value = not current_value
            setattr(settings, field.value, new_value)

            # Commit the change
            db.add(settings)
            await db.commit()

            return new_value

    @staticmethod
    async def get_node_excluded() -> List[str]:
        """
        Retrieve the list of excluded node monitorings.
        If settings don't exist, creates a new record with empty list.
        """
        async with get_db() as db:
            settings = await SettingManager._get_or_create_settings(db)
            return settings.node_excluded_monitorings or []

    @staticmethod
    async def update_node_excluded(excluded_nodes: List[str]) -> List[str]:
        """
        Update the list of excluded node monitorings.
        Creates settings record if it doesn't exist.
        """
        async with get_db() as db:
            settings = await SettingManager._get_or_create_settings(db)

            settings.node_excluded_monitorings = excluded_nodes
            await db.commit()
            await db.refresh(settings)

            return settings.node_excluded_monitorings
