from pydantic_settings import BaseSettings, SettingsConfigDict


class _KeyboardSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    HOMES: str = "🏛️ Home"
    SERVERS: str = "☁️ Servers"
    CREATE: str = "➕ Create"
    USERS: str = "👤 Users"