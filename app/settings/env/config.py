from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSetup(BaseSettings):
    """.env file config data"""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    BOT_TOKEN: str
    ADMINS_ID: list[int]

    def is_admin(self, chatid: int) -> bool:
        """check user is admin or not"""
        return chatid in self.ADMINS_ID
