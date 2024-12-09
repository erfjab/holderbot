from pydantic_settings import BaseSettings, SettingsConfigDict


class KeyboardTextSetup(BaseSettings):
    """keyboard text file config data"""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    SERVERS: str = "servers"
    NEW_SERVER: str = "new server"
    UPDATE_DATA: str = "update"
    CANCEL: str = "cancel"
