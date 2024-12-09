from pydantic_settings import BaseSettings, SettingsConfigDict


class MessageTextSetup(BaseSettings):
    """message text file config data"""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    HOME: str = "<b>👋 Welcome to HolderBot</b>"
    ASK_SERVER_REMARK: str = "<b>📝 Enter a unique server remark:</b>"
    ASK_SERVER_TYPE: str = "<b>☁️ Select Server Type:</b>"
    ASK_MARZ_SERVER_DATA: str = (
        "<b>🔐 Enter Marz Server Credentials:\n</b>"
        "• <code>Username [sudo]</code>\n"
        "• <code>Password [sudo]</code>\n"
        "• <code>Host [https://sub.domain.com:port]</code>\n\n"
        "<b>Example:</b>\n"
        "<code>erfan\nerfan\nhttps://panel.domain.com:443</code>"
    )
    WRONG_STRING_INPUT: str = "<b>❌ Invalid input!</b>"
    DUPLICATE: str = "<b>⚠️ Data already exists. Choose another...</b>"
    SERVER_WRONG_DATA_INPUT: str = (
        "<b>❌ Incorrect server data format. try again...</b>"
    )
    SUCCES: str = "<b>✅ Action is Succes!</b>"
    FAILED: str = "<b>❌ Action is Failed!</b>"
