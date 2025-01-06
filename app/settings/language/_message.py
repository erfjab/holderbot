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
    ITEMS: str = "Select items"
    MENU: str = "Select a Button"
    ASK_REMARK: str = "Enter remark: [a-z]"
    WRONG_STR: str = "❌ Invalid, Just use [a-z]"
    WRONG_INT: str = "❌ Invalid, Just use [0-9]"
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
    FAILED: str = "❌ Failed"
    NOT_FOUND: str = "❌ Not Found."
    ASK_COUNT: str = "Enter count: [0-9]"
    ASK_SUFFIX: str = "Enter Suffix:"
    ASK_DATA_LIMT: str = "Enter DataLimit: [0-9]\n0 for unlimited"
    ASK_DATE_LIMIT: str = "Enter DateLimit: [0-9]"
    ASK_CONFIGS: str = "Select Configs:"
    FAILED_USERNAME: str = "❌ Failed to create {username}."
    USER_INFO: str = (
        "• <b>Username:</b> <code>{username}</code>\n"
        "• <b>Data Limit:</b> <code>{data_limit}</code>\n"
        "• <b>Date Limit:</b> <code>{expire_strategy}</code>\n"
        "• <b>Sub Url:</b> <code>{subscription_url}</code>\n"
    )
