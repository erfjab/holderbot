"""
This module provides functionality for managing settings in the application.

It includes methods for upserting and retrieving settings from the database.
"""

from sqlalchemy.future import select
from db.base import get_db
from db.models import Setting
from models import SettingData, SettingUpsert, SettingKeys


class SettingManager:
    """Manager class for handling settings operations."""

    @staticmethod
    async def upsert(setting_upsert: SettingUpsert) -> SettingData | None:
        """
        Upsert a setting in the database.

        If the setting exists and the value is None, it will be deleted.
        If the setting does not exist, it will be created.

        Args:
            setting_upsert (SettingUpsert): The setting data to upsert.

        Returns:
            SettingData | None: The upserted setting data or None if deleted.
        """
        async with get_db() as db:
            existing_setting = await db.execute(
                select(Setting).where(Setting.key == setting_upsert.key)
            )
            setting = existing_setting.scalar_one_or_none()

            if setting:
                if setting_upsert.value is None:
                    await db.delete(setting)
                    await db.commit()
                    return None
                setting.value = setting_upsert.value
            else:
                if setting_upsert.value is not None:
                    setting = Setting(
                        key=setting_upsert.key, value=setting_upsert.value
                    )
                    db.add(setting)

            await db.commit()
            await db.refresh(setting)
            return SettingData.from_orm(setting)

    @staticmethod
    async def get(key: SettingKeys) -> SettingData | None:
        """
        Retrieve a setting by its key.

        Args:
            key (SettingKeys): The key of the setting to retrieve.

        Returns:
            SettingData | None: The retrieved setting data or None if not found.
        """
        async with get_db() as db:
            result = await db.execute(select(Setting).where(Setting.key == key))
            setting = result.scalar_one_or_none()
            return SettingData.from_orm(setting) if setting else None
