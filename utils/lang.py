from enum import Enum

VERSION = "0.2.1"
OWNER = "@ErfJabs"


class KeyboardTexts(str, Enum):
    Home = "🏠 Back to home"
    UserCreate = "👤 User Create"
    NodeMonitoring = "🗃 Node Monitoring"
    Active = "✅ Active"
    OnHold = "⏸️ On hold"
    Finish = "✔️ Finish"
    NodeMonitoringChecker = "🧨 Checker"
    NodeMonitoringAutoRestart = "🔁 AutoRestart"
    UsersMenu = "👥 Users"
    UsersAddInbound = "➕ Add inbound"
    UsersDeleteInbound = "➖ Delete inbound"


class MessageTexts(str, Enum):
    Start = f"Welcome to <b>HolderBot</b> 🤖 [{VERSION}]\nDeveloped and designed by <b>{OWNER}</b>"
    Version = f"⚡️ <b>Current Version:</b> <code>{VERSION}</code>"
    AskCreateUserBaseUsername = "👤 Please enter the <b>user base name</b>"
    AskCreateUserStartNumber = "🔢 Please enter the <b>starting user number</b>"
    AskCreateUserHowMuch = "👥 How many users would you like to create?"
    AskCreateUserDataLimit = "📊 Please enter the <b>data limit</b> in GB"
    AskCreateUserDateLimit = "📅 Please enter the <b>date limit</b> in days"
    AskCreateUserStatus = "🔄 Select the <b>user status</b>"
    AskCreateAdminUsername = "👤 Select the <b>owner admin</b>"
    AskCreateUserInbouds = "🌐 Select the <b>user inbounds</b>"
    JustNumber = "🔢 Please enter <b>numbers only</b>"
    NoneUserInbounds = "⚠️ Please select an <b>inbound</b> first"
    UserInfo = (
        "{status_emoji} <b>Username:</b> <code>{username}</code>\n"
        "📊 <b>Data limit:</b> <code>{data_limit}</code> GB\n"
        "📅 <b>Date limit:</b> <code>{date_limit}</code> days\n"
        "🔗 <b>Subscription:</b> {subscription}"
    )
    NodeError = (
        "🗃 <b>Node:</b> <code>{name}</code>\n"
        "📍 <b>IP:</b> <code>{ip}</code>\n"
        "📪 <b>Message:</b> <code>{message}</code>"
    )
    NodeAutoRestartDone = "✅ <code>{name}</code> <b>auto restart is Done!</b>"
    NodeAutoRestartError = "❌ <code>{name}</code> <b>auto restart is Wrong!</b>"
    NodeMonitoringMenu = (
        "🧨 <b>Checker is</b> <code>{checker}</code>\n"
        "🔁 AutoRestart is <code>{auto_restart}</code>"
    )
    UsersMenu = "👥 What do you need?"
    UsersInboundSelect = "🌐 Select Your Inbound:"
    Working = "⏳"
    UsersInboundSuccessUpdated = "✅ Users Inbounds is Updated!"
    UsersInboundErrorUpdated = "❌ Users Inbounds not Updated!"
