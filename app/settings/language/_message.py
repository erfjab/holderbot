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
    MENU: str = "Select a Button"
    ASK_REMARK: str = "Enter remark: [a-z]"
    WRONG_STR: str = "❌ Invalid, Just use [a-z]"
    DUPLICATE: str = "❌ Duplicate, try another."
    ASK_TYPES: str = "Select a type:"
    ASK_MARZNESHIN_DATA: str = (
        "<b>Enter Marzneshin Server Credentials:\n</b>"
        "• <code>Username [sudo]</code>\n"
        "• <code>Password [sudo]</code>\n"
        "• <code>Host [https://sub.domain.com:port]</code>\n\n"
        "<b>Example:</b>\n"
        "<code>erfan\nerfan\nhttps://panel.domain.com:443</code>"
    )
    WRONG_PATTERN: str = "❌ Invalid pattern."
    INVALID_DATA: str = "❌ Invalid data."
    SUCCESS: str = "✅ Success."
    FAILED: str = "❌ Failed."
    NOT_FOUND: str = "❌ Not Found."
