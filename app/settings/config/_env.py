from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettingsFile(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )
    DEBUG: bool = False
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_ADMINS_ID: list[int] = []
    QR_BACKGROUND: str = ""

    def is_admin(self, chatid: int) -> bool:
        return chatid in self.TELEGRAM_ADMINS_ID
