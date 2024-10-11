from enum import Enum

VERSION = "0.1.0"
OWNER = "@ErfJabs"


class KeyboardTexts(str, Enum):
    Home = "🏠 back to home"
    UserCreate = "👤 user create"
    Active = "✅ active"
    OnHold = "⏸️ on hold"
    Finish = "✔️ finish"


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
