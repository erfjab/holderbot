from decouple import config


# Function to check if a required configuration value is missing
def require_setting(setting_name, value):
    if not value:
        raise ValueError(
            f"The '{setting_name}' setting is required and cannot be empty."
        )


# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN", cast=str)  # required
require_setting("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN)

TELEGRAM_ADMINS_ID = config(
    "TELEGRAM_ADMINS_ID",
    default="",
    cast=lambda v: [
        int(i) for i in filter(str.isdigit, (s.strip() for s in v.split(",")))
    ],
)  # required
require_setting("TELEGRAM_ADMINS_ID", TELEGRAM_ADMINS_ID)

# Marzban Panel Settings
MARZBAN_USERNAME = config("MARZBAN_USERNAME", default="", cast=str)  # required
require_setting("MARZBAN_USERNAME", MARZBAN_USERNAME)

MARZBAN_PASSWORD = config("MARZBAN_PASSWORD", default="", cast=str)  # required
require_setting("MARZBAN_PASSWORD", MARZBAN_PASSWORD)

MARZBAN_ADDRESS = config("MARZBAN_ADDRESS", default="", cast=str)  # required
require_setting("MARZBAN_ADDRESS", MARZBAN_ADDRESS)

EXCLUDED_MONITORINGS = [
    x.strip()
    for x in config("EXCLUDED_MONITORINGS", default="", cast=str).split(",")
    if x.strip()
]
