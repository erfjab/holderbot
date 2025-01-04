from pydantic_settings import BaseSettings, SettingsConfigDict


class _KeyboardSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    HOMES: str = "🏛️ Home"
    SERVER: str = "☁️ Server"
    CREATE: str = "➕ Create"
    USERS: str = "👤 Users"
    DONE: str = "✔️ DONE"
