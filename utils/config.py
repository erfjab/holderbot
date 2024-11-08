"""
This module contains configuration settings for the application, including
Telegram bot settings, Marzban panel settings, and excluded monitorings.
It ensures that all required settings are provided and checks for missing values.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvFile(BaseSettings):
    """.env file config data"""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMINS_ID: list[int]
    MARZBAN_USERNAME: str
    MARZBAN_PASSWORD: str
    MARZBAN_ADDRESS: str
    ACTION_LIMIT: int = 25
