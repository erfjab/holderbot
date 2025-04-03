from pydantic_settings import BaseSettings, SettingsConfigDict
from app.version import __version__


class _MessageSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    START: str = (
        f"Welcome to HolderBot 🤖 [<code>{__version__}</code> n"
        "<b><a href='"
    )
    ny Config."
    ASK_COUNT: str = "تعداد را وارد کنید [0-9]"
    ASK_SUFFIX: str = "پسوند را وارد کنید:"
    ASK_DATA_LIMT: str = "محدودیت داده را وارد کنید: [0-9]\n0 for unlimited"
    ASK_DATE_LIMIT: str = "محدودیت تاریخ را وارد کنید: [0-9]"
    ASK_CONFIGS: str = "پیکربندی‌ها را انتخاب کنید:"
    FAILED_USERNAME: str = "❌ ایجاد نشد {username}."
    RANDOM_USERNAME: str = "نام کاربری تصادفی"
    USER_INFO: str = (
        "• <b>Username:</b> <code>{username}</code>\n"
        "• <b>Data Limit:</b> <code>{data_limit}</code>\n"
        "• <b>Date Limit:</b> <code>{expire_strategy}</code>\n"
        "• <b>Sub Url:</b> <code>{subscription_url}</code>\n"
    )
    ASK_SURE: str = "آیا مطمئن هستید?"
    ASK_ADMIN: str = "مدیر را انتخاب کنید:"
    ASK_NOTE: str = "متن یادداشت را وارد کنید"
    ASK_ADMIN_FROM: str = "از بین مدیران انتخاب کنید:"
    ASK_ADMIN_TO: str = "Select to admin:ITEMS_MENU: str = "Select a item or create a new:"
    ITEMS: str = "یک گزینه را انتخاب کنید"
    MENU: str = "یک دکمه را انتخاب کنید"
    ASK_REMARK: str = "نام کاربر را وارد کنید: [a-z]"
    ASK_JSON: str = "فایل json را وارد کنید: [*.json]"
    CREATE_WITH_JSON: str = "ایجاد با .Json"
    INVALID_JSON: str = "❌ نا معتبر است  json."
    WORNG_DOC: str = "❌ نامعتبر است,   فقظ doc"
    WORNG_JSON: str = "❌ نامعتبر است فقط [*.json]"
    WRONG_STR: str = "❌ نامعتبر است ، فقط از [a-z]"
    WRONG_INT: str = "❌ نامعتبر است، فقط از [0-9] استفاده کنید"
    DUPLICATE: str = "❌   تکراری است، گزینه دیگری امتحان کنید. "
    ASK_TYPES: str = "یک نوع را انتخاب کنید:"
    ASK_MARZ_DATA: str = (
        "<b>Enter Marz Server Credentials:\n</b>"
        "• <code>Username [sudo]</code>\n"
        "• <code>Password [sudo]</code>\n"
        "• <code>Host [https://sub.domain.com:port]</code>\n\n"
        "<b>Example:</b>\n"
        "<code>erfan\nerfan\nhttps://panel.domain.com:443</code>"
    )
    WRONG_PATTERN: str = "❌ رمز شما نامعتبر است"
    INVALID_DATA: str = "❌داده نامعتبر است."
    SUCCESS: str = "✅ موفقیت‌آمیز."
    FAILED: str = "❌ ناموفق"
    NOT_FOUND: str = "❌ یافت نشد."
    NOT_FOUND_CONFIGS: str = "❌ هیچ پیکربندی‌ای یافت نشد"
    ASK_USERNAME: str = "نام کاربری را وارد کنید:"
