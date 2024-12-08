from pydantic_settings import BaseSettings, SettingsConfigDict


class MessageTextSetup(BaseSettings):
    """message text file config data"""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    HOME: str = "Hi, Welcome to holderbot"
