from pydantic_settings import BaseSettings, SettingsConfigDict

class _KeyboardSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    HOMES: str = "🏛️ خانه"
    SERVER: str = "☁️ سرور"
    CREATE: str = "➕ ایجاد"
    USERS: str = "👤 کاربران"
    ACTIONS: str = "🗄 عملیات"
    CREATE_USER: str = "➕ ساخت کاربر"
    SEARCH_USER: str = "🔍 جستجوی کاربر"
    CREATE_SERVER: str = "➕ افزودن سرور"
    TEMPLATES: str = "🗃 قالب‌ها"
    DONE: str = "✔️ انجام شد"
    LEFT: str = "⬅️"
    RIGHT: str = "➡️"
    UPDATE_CHECKER: str = "👀 بررسی بروزرسانی"
    STATS: str = "📊 آمار"
    SELECTS_ALL: str = "انتخاب همه"
    DESELECTS_ALL: str = "لغو انتخاب همه"
    BACK: str = "◀️ بازگشت"
