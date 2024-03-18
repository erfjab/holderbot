from pyrogram.types import *
from Function.db import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

KEYBOARD_HOME = ReplyKeyboardMarkup([[KeyboardButton("🚀 Create User"),KeyboardButton("🎖 Notice")],
    [KeyboardButton("👤 Users"), KeyboardButton("👨🏻‍💻 Admins"), KeyboardButton("🎗 Nodes")],
    [KeyboardButton("🗃 Templates"),KeyboardButton("🎛 Monitoring")],
    [KeyboardButton("🔍 Search"), KeyboardButton("💬 Help"), KeyboardButton("🖼 QR Code")]], resize_keyboard=True)


KEYBOARD_CANCEL = ReplyKeyboardMarkup([[KeyboardButton("🔙 cancel")]] , resize_keyboard=True)


def KEYBOARD_ADMINS_LIST(CHATID) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/admins"
    RESPONCE = requests.get(url=URL, headers=PANEL_TOKEN , verify=False)
    if RESPONCE.status_code == 200:
        RESPONCE_DATA = RESPONCE.json()
        KEYBOARD_ADMINS_LIST = []
        for ADMIN in RESPONCE_DATA:
            SUDO = "SUDO" if ADMIN.get("is_sudo") else "N.SUDO"
            KEYBOARD_ADMINS_LIST.append([KeyboardButton(f"{ADMIN.get('username')} - {SUDO}")])
        KEYBOARD_ADMINS_LIST.append([KeyboardButton("🔙 cancel") , KeyboardButton("➕ Add new admin")])
        KEYBOARD_ADMINS_LIST = ReplyKeyboardMarkup(KEYBOARD_ADMINS_LIST, resize_keyboard=True)
        return KEYBOARD_ADMINS_LIST
    
KEYBOARD_ADMIN = ReplyKeyboardMarkup([[KeyboardButton("🔐 Change pass"),KeyboardButton("🔐 Change sudo")],
    [KeyboardButton("🗑 Delete admin")],
    [KeyboardButton("🔙 cancel")]] , resize_keyboard=True)

KEYBOARD_YES_OR_NOO = ReplyKeyboardMarkup([[KeyboardButton("✅ YES , sure!"),KeyboardButton("❌ NO ,forget.")],
    [KeyboardButton("🔙 cancel")]] , resize_keyboard=True)

KEYBOARD_SUDO = ReplyKeyboardMarkup([[KeyboardButton("✅ YES , is sudo!"),KeyboardButton("❌ NO , not sudo.")],
    [KeyboardButton("🔙 cancel")]] , resize_keyboard=True)

KEYBOARD_USERS = ReplyKeyboardMarkup([[KeyboardButton("✅ Active list"), KeyboardButton("❌ Disabled list")],
    [KeyboardButton("🕰 Expired"), KeyboardButton("🪫 Limited"), KeyboardButton("🔌 On Hold")],
    [KeyboardButton("👀 Online time list"), KeyboardButton("📡 Sub Update list")],
    [KeyboardButton("🔙 cancel")]] , resize_keyboard=True)

KEYBOARD_LIST_TIMES = ReplyKeyboardMarkup([[KeyboardButton("1 min"), KeyboardButton("5 min"), KeyboardButton("15 min"), KeyboardButton("30 min")],
    [KeyboardButton("1 hour"), KeyboardButton("3 hour"), KeyboardButton("6 hour"), KeyboardButton("12 hour")],
    [KeyboardButton("1 day"), KeyboardButton("3 day"), KeyboardButton("7 day"), KeyboardButton("14 day")],
    [KeyboardButton("21 day"), KeyboardButton("30 day"), KeyboardButton("45 day"), KeyboardButton("60 day")],
    [KeyboardButton("🔙 cancel")]] , resize_keyboard=True)

def DEF_NODES_LIST(CHATID) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/nodes"
    RESPONCE = requests.get(url=URL, headers=PANEL_TOKEN , verify=False)
    if RESPONCE.status_code == 200:
        RESPONCE_DATA = RESPONCE.json()
        KEYBOARD_NODES_LIST = []
        for NODE in RESPONCE_DATA:
            KEYBOARD_NODES_LIST.append([KeyboardButton(f"( {NODE.get('id')} ) {NODE.get('name')} - {NODE.get('address')}")])
        KEYBOARD_NODES_LIST.append([KeyboardButton("🔙 cancel")])
        KEYBOARD_NODES_LIST = ReplyKeyboardMarkup(KEYBOARD_NODES_LIST, resize_keyboard=True)
        return KEYBOARD_NODES_LIST
    
KEYBOARD_NODE = ReplyKeyboardMarkup([[KeyboardButton("🔏 Usage Coefficient"),KeyboardButton("📊 Status")],
    [KeyboardButton("✅ Activate"), KeyboardButton("⚡️ Reconnect"), KeyboardButton("❌ Disable")],
    [KeyboardButton("🔙 cancel")]] , resize_keyboard=True)


KEYBOARD_ON_MONITORING = ReplyKeyboardMarkup([[KeyboardButton("🔴 Disable monitoring")],
        [KeyboardButton("⏱ Error timer"), KeyboardButton("⏱ Normal timer")],
        [KeyboardButton("🔙 cancel")]] , resize_keyboard=True)


KEYBOARD_OFF_MONITORING = ReplyKeyboardMarkup([[KeyboardButton("🟢 Monitoring activation")],
        [KeyboardButton("🔙 cancel")]] , resize_keyboard=True)

def KEYBOARD_TEMPLATES_LIST() :
    TEMPLATES = DEF_TEMPLATES_DATA()
    KEYBOARD_TEMPLATES_LIST = []
    for TEMPLATE in TEMPLATES :
        TEMPLATE_NAME, TEMPLATE_DATA , TEMPLATE_DATE = TEMPLATE
        KEYBOARD_TEMPLATES_LIST.append([KeyboardButton(f"{TEMPLATE_NAME} - {TEMPLATE_DATA} GB {TEMPLATE_DATE} days")])
    KEYBOARD_TEMPLATES_LIST.append([KeyboardButton("🔙 cancel") , KeyboardButton("➕ Add new tempalte")])
    KEYBOARD_TEMPLATES_LIST = ReplyKeyboardMarkup(KEYBOARD_TEMPLATES_LIST, resize_keyboard=True)
    return KEYBOARD_TEMPLATES_LIST 


KEYBOARD_TEMPLATE = ReplyKeyboardMarkup([[KeyboardButton("🗑 Delete Template")],
        [KeyboardButton("🔙 cancel")]] , resize_keyboard=True)


def KEYBOARD_ALL_INBOUNDS(INBOUNDS_ALL , INBOUNDS_SELECT , SELECTED_TAG , BACK_NAME) :
    KEYBOARD_SELECT , KEYBOARD_NOT_SELECT = ["➕","➖"]

    KEYBOARD_COLUMNS = 2
    KEYBOARD_ROWS = (len(INBOUNDS_ALL) + KEYBOARD_COLUMNS - 1) // KEYBOARD_COLUMNS

    if SELECTED_TAG :
        INBOUNDS_SELECT[SELECTED_TAG] = not INBOUNDS_SELECT[SELECTED_TAG]    
        KEYBOARD_INBOUNDS = [
            [InlineKeyboardButton(f"{KEYBOARD_SELECT if INBOUNDS_SELECT[TAG] else KEYBOARD_NOT_SELECT} {TAG}", callback_data=f"{BACK_NAME} tag {TAG}") for TAG in INBOUNDS_ALL[KEYBOARD_ROWS * KEYBOARD_COLUMNS:(KEYBOARD_ROWS + 1) * KEYBOARD_COLUMNS]]
            for KEYBOARD_ROWS in range(KEYBOARD_ROWS)]
    
    else :
        KEYBOARD_INBOUNDS = [
                [InlineKeyboardButton(f"{KEYBOARD_SELECT} {TAG}", callback_data=f"{BACK_NAME} tag {TAG}") for TAG in INBOUNDS_ALL[KEYBOARD_ROWS * KEYBOARD_COLUMNS:(KEYBOARD_ROWS + 1) * KEYBOARD_COLUMNS]]
                for KEYBOARD_ROWS in range(KEYBOARD_ROWS)
            ]
    
    KEYBOARD_INBOUNDS.append([
        InlineKeyboardButton("❌ cancel", callback_data=f"{BACK_NAME} no"),
        InlineKeyboardButton("✅ finish", callback_data=f"{BACK_NAME} yes")
    ])
    return InlineKeyboardMarkup(KEYBOARD_INBOUNDS)

def KEYBOARD_TEMPLATES_LIST() :
    TEMPLATES = DEF_TEMPLATES_DATA()
    KEYBOARD_TEMPLATES_LIST = []
    for TEMPLATE in TEMPLATES :
        TEMPLATE_NAME, TEMPLATE_DATA , TEMPLATE_DATE = TEMPLATE
        KEYBOARD_TEMPLATES_LIST.append([KeyboardButton(f"{TEMPLATE_NAME} - {TEMPLATE_DATA} GB {TEMPLATE_DATE} days")])
    KEYBOARD_TEMPLATES_LIST.append([KeyboardButton("🔙 cancel") , KeyboardButton("➕ Add new tempalte")])
    KEYBOARD_TEMPLATES_LIST = ReplyKeyboardMarkup(KEYBOARD_TEMPLATES_LIST, resize_keyboard=True)
    return KEYBOARD_TEMPLATES_LIST

def KEYBOARD_CREATE_LIST() :
    TEMPLATES = DEF_TEMPLATES_DATA()
    KEYBOARD_TEMPLATES_LIST = []
    KEYBOARD_TEMPLATES_LIST.append([KeyboardButton("🚀 Manual")])
    for TEMPLATE in TEMPLATES :
        TEMPLATE_NAME, TEMPLATE_DATA , TEMPLATE_DATE = TEMPLATE
        KEYBOARD_TEMPLATES_LIST.append([KeyboardButton(f"{TEMPLATE_NAME} - {TEMPLATE_DATA} GB {TEMPLATE_DATE} days")])
    KEYBOARD_TEMPLATES_LIST.append([KeyboardButton("🔙 cancel")])
    KEYBOARD_TEMPLATES_LIST = ReplyKeyboardMarkup(KEYBOARD_TEMPLATES_LIST, resize_keyboard=True)
    return KEYBOARD_TEMPLATES_LIST

KEYBOARD_CREATE_MUCH = ReplyKeyboardMarkup([[KeyboardButton("1"), KeyboardButton("2"), KeyboardButton("3"), KeyboardButton("4"), KeyboardButton("5"), KeyboardButton("6")],
    [KeyboardButton("7"), KeyboardButton("8"), KeyboardButton("9"), KeyboardButton("10"), KeyboardButton("11"), KeyboardButton("12")],
    [KeyboardButton("13"), KeyboardButton("14"), KeyboardButton("15"), KeyboardButton("16"), KeyboardButton("17"), KeyboardButton("18")],
    [KeyboardButton("20"), KeyboardButton("25"), KeyboardButton("30"), KeyboardButton("35"), KeyboardButton("40"), KeyboardButton("50")],
    [KeyboardButton("🔙 cancel")]] , resize_keyboard=True)

KEYBOARD_MESSAGES = ReplyKeyboardMarkup([[KeyboardButton("👀 change status") , KeyboardButton("🔙 cancel")]] , resize_keyboard=True)
