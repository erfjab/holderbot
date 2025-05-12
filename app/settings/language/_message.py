from pydantic_settings import BaseSettings, SettingsConfigDict
from app.version import __version__


class _MessageSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    START: str = (
        f"به هولدر بات خوش اومدی 🤖 [<code>{__version__}</code> توسط ]\n"
        "<b><a href=''></a></b>"
    )
    LETS_BACK: str = "بریم عقب..."
    ITEMS_MENU: str = "یه مورد انتخاب کن یا مورد جدید بساز:"
    ITEMS: str = "موردها رو انتخاب کن"
    MENU: str = "یه دکمه انتخاب کن"
    ASK_REMARK: str = "توضیح وارد کن: [a-z]"
    ASK_JSON: str = "فایل JSON رو وارد کن: [*.json]"
    CREATE_WITH_JSON: str = "ساختن با JSON"
    INVALID_JSON: str = "❌ فایل JSON نامعتبره."
    WORNG_DOC: str = "❌ نامعتبر، فقط فایل داکیومنت بفرست"
    WORNG_JSON: str = "❌ نامعتبر، فقط از [*.json] استفاده کن"
    WRONG_STR: str = "❌ نامعتبر، فقط حروف [a-z] مجازه"
    WRONG_INT: str = "❌ نامعتبر، فقط اعداد [0-9] مجازه"
    DUPLICATE: str = "❌ تکراریه، یه چیز دیگه امتحان کن."
    ASK_TYPES: str = "یه نوع انتخاب کن:"
    ASK_MARZ_DATA: str = (
        "<b>اطلاعات سرور مرز رو وارد کن:\n</b>"
        "• <code>نام کاربری [sudo]</code>\n"
        "• <code>رمز عبور [sudo]</code>\n"
        "• <code>آدرس سرور [https://sub.domain.com:port]</code>\n\n"
        "<b>مثال:</b>\n"
        "<code>erfan\nerfan\nhttps://panel.domain.com:443</code>"
    )
    WRONG_PATTERN: str = "❌ الگوی واردشده نامعتبره."
    INVALID_DATA: str = "❌ داده نامعتبره."
    SUCCESS: str = "✅ با موفقیت انجام شد."
    FAILED: str = "❌ ناموفق بود"
    NOT_FOUND: str = "❌ پیدا نشد."
    NOT_FOUND_CONFIGS: str = "❌ هیچ کانفیگی پیدا نشد."
    ASK_COUNT: str = "تعداد رو وارد کن: [0-9]"
    ASK_SUFFIX: str = "پسوند رو وارد کن:"
    ASK_DATA_LIMT: str = "حجم مجاز رو وارد کن: [0-9]\n۰ برای نامحدود"
    ASK_DATE_LIMIT: str = "تاریخ انقضا رو وارد کن: [0-9]"
    ASK_CONFIGS: str = "کانفیگ‌هارو انتخاب کن:"
    FAILED_USERNAME: str = "❌ ایجاد کاربر {username} ناموفق بود."
    RANDOM_USERNAME: str = "نام کاربری تصادفی"
    USER_INFO: str = (
        "• <b>نام کاربری:</b> <code>{username}</code>\n"
        "• <b>حجم مجاز:</b> <code>{data_limit}</code>\n"
        "• <b>محدودیت زمانی:</b> <code>{expire_strategy}</code>\n"
        "• <b>لینک اشتراک:</b> <code>{subscription_url}</code>\n"
    )
    ASK_SURE: str = "مطمئنی؟"
    ASK_ADMIN: str = "ادمین رو انتخاب کن:"
    ASK_NOTE: str = "متن یادداشت رو وارد کن:"
    ASK_ADMIN_FROM: str = "ادمین مبدا رو انتخاب کن:"
    ASK_ADMIN_TO: str = "ادمین مقصد رو انتخاب کن:"
    ASK_USERNAME: str = "نام کاربری رو وارد کن:"
