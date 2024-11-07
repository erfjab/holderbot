"""
This module provides functionality for managing application settings,
including methods for updating and retrieving settings.
"""

from sqlalchemy.future import select
from db.base import get_db
from db.models import Setting
from models import SettingKeys


class SettingManager:
    """Handles the application's settings management, ensuring a single settings record exists."""

    @staticmethod
    async def get(field: SettingKeys) -> bool:
        """
        Retrieve the specified setting field, ensuring the settings record exists.
        If the settings record does not exist, it will be created.
        """
        async with get_db() as db:
            # Attempt to retrieve the settings record
            result = await db.execute(select(Setting))
            settings = result.scalar_one_or_none()

            # If no settings record, create it
            if not settings:
                settings = Setting()
                db.add(settings)
                await db.commit()
                await db.refresh(settings)  # Refresh after commit to access attributes

            # Return the value of the specified field
            return getattr(settings, field.value)

    @staticmethod
    async def toggle_field(field: SettingKeys) -> bool:
        """
        Toggle a boolean setting field and return its new value.
        Ensures the settings record exists before toggling.
        """
        async with get_db() as db:
            # Retrieve or create the settings record
            result = await db.execute(select(Setting))
            settings = result.scalar_one_or_none()

            if not settings:
                settings = Setting()
                db.add(settings)
                await db.commit()
                await db.refresh(settings)

            # Toggle the field's current value
            current_value = getattr(settings, field.value)
            new_value = not current_value
            setattr(settings, field.value, new_value)

            # Commit the change
            db.add(settings)
            await db.commit()

            return new_value