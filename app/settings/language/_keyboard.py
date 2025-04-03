from pydantic_settings import BaseSettings, SettingsConfigDict


class _KeyboardSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    HOMES: str = "🏛️ خانه"
    SERVER: str = "☁️ سرور"
    CREATE: str = "➕ ایجاد"
    USERS: str = "👤 کاربران"
    ACTIONS: str = "🗄 Actions"
    CREATE_USER: str = "➕ ایجاد کاربر"
    SEARCH_USER: str = "🔍 جستجوی کاربر"
    CREATE_SERVER: str = "➕ اضافه کردن سرور"
    TEMPLATES: str = "🗃 قالب "
    DONE: str = "✔️ انجام شد"
    LEFT: str = "⬅️"
    RIGHT: str = "➡️"
    UPDATE_CHECKER: str = "👀 به روز رسانی را بررسی کنید"
    STATS: str = "📊 آمار"
    SELECTS_ALL: str = "انتخاب همه "
    DESELECTS_ALL: str = "لغو همه"
    BACK: str = "◀️ بازگشت"
