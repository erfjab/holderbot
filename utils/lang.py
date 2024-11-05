"""
This module contains constants and texts used in the HolderBot.
"""

from enum import Enum

# Module constants
VERSION = "0.2.3"
OWNER = "@ErfJabs"


class KeyboardTexts(str, Enum):
    """Keyboard texts used in the bot."""

    HOME = "🏠 Back to home"
    USER_CREATE = "👤 User Create"
    NODE_MONITORING = "🗃 Node Monitoring"
    ACTIVE = "✅ Active"
    ON_HOLD = "⏸️ On hold"
    FINISH = "✔️ Finish"
    NODE_MONITORING_CHECKER = "🧨 Checker"
    NODE_MONITORING_AUTO_RESTART = "🔁 AutoRestart"
    USERS_MENU = "👥 Users"
    USERS_ADD_INBOUND = "➕ Add inbound"
    USERS_DELETE_INBOUND = "➖ Delete inbound"
    USER_CREATE_LINK_COPY = "To copy the link, please click."


class MessageTexts(str, Enum):
    """Message texts used in the bot."""

    START = f"Welcome to <b>HolderBot</b> 🤖 [{VERSION}]\nDeveloped and designed by <b>{OWNER}</b>"
    VERSION = f"⚡️ <b>Current Version:</b> <code>{VERSION}</code>"
    ASK_CREATE_USER_BASE_USERNAME = "👤 Please enter the <b>user base name</b>"
    ASK_CREATE_USER_START_NUMBER = "🔢 Please enter the <b>starting user number</b>"
    ASK_CREATE_USER_HOW_MUCH = "👥 How many users would you like to create?"
    ASK_CREATE_USER_DATA_LIMIT = "📊 Please enter the <b>data limit</b> in GB"
    ASK_CREATE_USER_DATE_LIMIT = "📅 Please enter the <b>date limit</b> in days"
    ASK_CREATE_USER_STATUS = "🔄 Select the <b>user status</b>"
    ASK_CREATE_ADMIN_USERNAME = "👤 Select the <b>owner admin</b>"
    ASK_CREATE_USER_INBOUNDS = "🌐 Select the <b>user inbounds</b>"
    JUST_NUMBER = "🔢 Please enter <b>numbers only</b>"
    NONE_USER_INBOUNDS = "⚠️ Please select an <b>inbound</b> first"
    USER_INFO = (
        "{status_emoji} <b>Username:</b> <code>{username}</code>\n"
        "📊 <b>Data limit:</b> <code>{data_limit}</code> GB\n"
        "📅 <b>Date limit:</b> <code>{date_limit}</code> days\n"
        "🔗 <b>Subscription:</b> {subscription}"
    )
    NODE_ERROR = (
        "🗃 <b>Node:</b> <code>{name}</code>\n"
        "📍 <b>IP:</b> <code>{ip}</code>\n"
        "📪 <b>Message:</b> <code>{message}</code>"
    )
    NODE_AUTO_RESTART_DONE = "✅ <code>{name}</code> <b>auto restart is Done!</b>"
    NODE_AUTO_RESTART_ERROR = "❌ <code>{name}</code> <b>auto restart is Wrong!</b>"
    NODE_MONITORING_MENU = (
        "🧨 <b>Checker is</b> <code>{checker}</code>\n"
        "🔁 AutoRestart is <code>{auto_restart}</code>"
    )
    USERS_MENU = "👥 What do you need?"
    USERS_INBOUND_SELECT = "🌐 Select Your Inbound:"
    WORKING = "⏳"
    USERS_INBOUND_SUCCESS_UPDATED = "✅ Users Inbounds is Updated!"
    USERS_INBOUND_ERROR_UPDATED = "❌ Users Inbounds not Updated!"
