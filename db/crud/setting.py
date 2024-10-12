from sqlalchemy.future import select
from db.base import GetDB
from db.models import Setting
from models import SettingData, SettingUpsert, SettingKeys


class SettingManager:

    @staticmethod
    async def upsert(setting_upsert: SettingUpsert) -> SettingData | None:
        async with GetDB() as db:
            existing_setting = await db.execute(
                select(Setting).where(Setting.key == setting_upsert.key)
            )
            setting = existing_setting.scalar_one_or_none()

            if setting:
                if setting_upsert.value is None:
                    await db.delete(setting)
                    await db.commit()
                    return None
                else:
                    setting.value = setting_upsert.value
            else:
                if setting_upsert.value is None:
                    return None
                setting = Setting(key=setting_upsert.key, value=setting_upsert.value)
                db.add(setting)

            await db.commit()
            await db.refresh(setting)
            return SettingData.from_orm(setting)

    @staticmethod
    async def get(key: SettingKeys) -> SettingData:
        async with GetDB() as db:
            result = await db.execute(select(Setting).where(Setting.key == key))
            setting = result.scalar_one_or_none()
            return SettingData.from_orm(setting) if setting else None
