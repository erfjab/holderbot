"""
This module contains constants and texts used in the HolderBot.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class KeyboardTextsFile(BaseSettings):
    """Keyboard texts used in the bot."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    HOME: str = "🏠 Back to home"
    USER_CREATE: str = "👤 User Create"
    NODE_MONITORING: str = "🗃 Node Monitoring"
    ACTIVE: str = "✅ Active"
    ON_HOLD: str = "⏸️ On hold"
    FINISH: str = "✔️ Finish"
    NODE_MONITORING_CHECKER: str = "🧨 Checker"
    NODE_MONITORING_AUTO_RESTART: str = "🔁 AutoRestart"
    USERS_MENU: str = "👥 Users"
    USERS_ADD_INBOUND: str = "➕ Add inbound"
    USERS_DELETE_INBOUND: str = "➖ Delete inbound"
    USER_CREATE_LINK_COPY: str = "To copy the link, please click."


class MessageTextsFile(BaseSettings):
    """Message texts used in the bot."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    VERSION_NUMBER: str = "0.2.3"
    OWNER_ID: str = "@ErfJabs"

    START: str = (
        f"Welcome to <b>HolderBot</b> 🤖 [{VERSION_NUMBER}]\n"
        f"Developed and designed by <b>{OWNER_ID}</b>"
    )
    VERSION: str = f"⚡️ <b>Current Version:</b> <code>{VERSION_NUMBER}</code>"
    ASK_CREATE_USER_BASE_USERNAME: str = "👤 Please enter the <b>user base name</b>"
    ASK_CREATE_USER_START_NUMBER: str = (
        "🔢 Please enter the <b>starting user number</b>"
    )
    ASK_CREATE_USER_HOW_MUCH: str = "👥 How many users would you like to create?"
    ASK_CREATE_USER_DATA_LIMIT: str = "📊 Please enter the <b>data limit</b> in GB"
    ASK_CREATE_USER_DATE_LIMIT: str = "📅 Please enter the <b>date limit</b> in days"
    ASK_CREATE_USER_STATUS: str = "🔄 Select the <b>user status</b>"
    ASK_CREATE_ADMIN_USERNAME: str = "👤 Select the <b>owner admin</b>"
    ASK_CREATE_USER_INBOUNDS: str = "🌐 Select the <b>user inbounds</b>"
    JUST_NUMBER: str = "🔢 Please enter <b>numbers only</b>"
    NONE_USER_INBOUNDS: str = "⚠️ Please select an <b>inbound</b> first"
    USER_INFO: str = (
        "{status_emoji} <b>Username:</b> <code>{username}</code>\n"
        "📊 <b>Data limit:</b> <code>{data_limit}</code> GB\n"
        "📅 <b>Date limit:</b> <code>{date_limit}</code> days\n"
        "🔗 <b>Subscription:</b> {subscription}"
    )
    NODE_ERROR: str = (
        "🗃 <b>Node:</b> <code>{name}</code>\n"
        "📍 <b>IP:</b> <code>{ip}</code>\n"
        "📪 <b>Message:</b> <code>{message}</code>"
    )
    NODE_AUTO_RESTART_DONE: str = "✅ <code>{name}</code> <b>auto restart is Done!</b>"
    NODE_AUTO_RESTART_ERROR: str = (
        "❌ <code>{name}</code> <b>auto restart is Wrong!</b>"
    )
    NODE_MONITORING_MENU: str = (
        "🧨 <b>Checker is</b> <code>{checker}</code>\n"
        "🔁 AutoRestart is <code>{auto_restart}</code>"
    )
    USERS_MENU: str = "👥 What do you need?"
    USERS_INBOUND_SELECT: str = "🌐 Select Your Inbound:"
    WORKING: str = "⏳"
    USERS_INBOUND_SUCCESS_UPDATED: str = "✅ Users Inbounds is Updated!"
    USERS_INBOUND_ERROR_UPDATED: str = "❌ Users Inbounds not Updated!"
