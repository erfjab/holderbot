from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvSetup(BaseSettings):
    """.env file config data"""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    BOT_TOKEN: str
    ADMINS_ID: list[int]
