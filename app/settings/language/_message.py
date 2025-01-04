from pydantic_settings import BaseSettings, SettingsConfigDict


class _MessageSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    START: str = (
        "Welcome to HolderBot 🤖 [0.3.0]\n"
        "Developed and designed by <b>@ErfJabs</b>\n"
    )
    ITEMS_MENU: str = "Select a item or create a new:"
