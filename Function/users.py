from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from Function.db import *
from datetime import datetime
import requests , pytz , uuid

def DEF_PATCH_TO_SECEND(TIME) :
    ONLINE_PATCH = "%Y-%m-%dT%H:%M:%S.%f" if '.' in TIME else "%Y-%m-%dT%H:%M:%S"
    TIME = datetime.strptime(TIME , ONLINE_PATCH )
    TIME_UTC = pytz.utc.localize(TIME)
    TIME_LOCAL = TIME_UTC.astimezone(pytz.timezone('Asia/Tehran'))
    TIME_NOW = datetime.now(pytz.timezone('Asia/Tehran'))
    DELTA = TIME_NOW - TIME_LOCAL
    return DELTA

def DEF_ALL_USERS(CHATID) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/users"
    RESPONCE = requests.get(url=URL, headers=PANEL_TOKEN)
    LEN_ALL_USERS = LEN_ALL_ACTIVE_USERS = LEN_ALL_DISABLED_USERS = LEN_ALL_EXPIRED_USERS = LEN_ALL_LIMITED_USERS = LEN_ALL_ON_HOLD_USERS = LEN_ALL_ONLINE_USERS = LEN_ALL_OFFLINE_USERS = LEN_ALL_IS_UPDATE_USERS = LEN_ALL_NOT_UPDATE_USERS = 0
    if RESPONCE.status_code == 200 :
        RESPONCE_DATA = RESPONCE.json()
        for USER in RESPONCE_DATA["users"] :
            LEN_ALL_USERS += 1
            USER_STATUS = USER.get('status')
            if USER_STATUS == "active" :
                LEN_ALL_ACTIVE_USERS += 1
            elif USER_STATUS == "disabled":
                LEN_ALL_DISABLED_USERS += 1
            elif USER_STATUS == "expired" :
                LEN_ALL_EXPIRED_USERS += 1
            elif USER_STATUS == "limited" :
                LEN_ALL_LIMITED_USERS += 1
            elif USER_STATUS == "on_hold" :
                LEN_ALL_ON_HOLD_USERS += 1
            USER_ONLINE_AT = USER.get('online_at')
            if USER_ONLINE_AT :
                DELTA = (DEF_PATCH_TO_SECEND(USER_ONLINE_AT)).total_seconds()
                if int(DELTA) <= 86400 :
                    LEN_ALL_ONLINE_USERS += 1 
                else :
                    LEN_ALL_OFFLINE_USERS += 1
            USER_UPDATE_AT = USER.get('sub_updated_at')
            if USER_UPDATE_AT :
                DELTA = (DEF_PATCH_TO_SECEND(USER_UPDATE_AT)).total_seconds()
                if int(DELTA) <= 86400 :
                    LEN_ALL_IS_UPDATE_USERS += 1 
                else :
                    LEN_ALL_NOT_UPDATE_USERS += 1
        TEXT = f"<b>👤 All users :</b> {LEN_ALL_USERS}\n<b>✅ Active users :</b> {LEN_ALL_ACTIVE_USERS}\n<b>❌ Disables users :</b> {LEN_ALL_DISABLED_USERS}\n<b>🕰 Expired users :</b> {LEN_ALL_EXPIRED_USERS}\n<b>🪫 Limited users :</b> {LEN_ALL_LIMITED_USERS}\n<b>🔌 On hold users :</b> {LEN_ALL_ON_HOLD_USERS}\n\n<b>👀 Online users (last 24h) :</b> {LEN_ALL_ONLINE_USERS}\n<b>⚰️ Offline users (more 24h) :</b> {LEN_ALL_OFFLINE_USERS}\n\n<b>📡 Updated users (last 24h) :</b> {LEN_ALL_IS_UPDATE_USERS}\n<b>⚰️ Not Update users (more 24h) :</b> {LEN_ALL_NOT_UPDATE_USERS}"
    else :
        TEXT = f"<b>❌ I can't check users.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    return TEXT


def DEF_USERS_LIST_STATUS(MESSAGE_TEXT , CHATID) :
    USERS_LIST = {
        "✅ Active list": "active",
        "❌ Disabled list": "disabled",
        "🕰 Expired": "expired",
        "🪫 Limited": "limited",
        "🔌 On Hold": "on_hold"
    }    
    USERS_LIST_RESUTL = USERS_LIST.get(MESSAGE_TEXT)
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/users"
    RESPONCE = requests.get(url=URL, headers=PANEL_TOKEN)
    if RESPONCE.status_code == 200:
        RESPONCE_DATA = RESPONCE.json()
        LIST = []
        for USER in RESPONCE_DATA["users"] :
            USER_STATUS = USER.get('status')
            if USER_STATUS == USERS_LIST_RESUTL :
                USER_USERNAME = USER.get('username')
                LIST.append(USER_USERNAME)
        LIST.sort()
    else :
        LIST = []
    return LIST

def DEF_CREATE_PDF(user_list):
    pdf_name = str(uuid.uuid4()) + ".pdf"
    pdf = SimpleDocTemplate(pdf_name, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    data = [user_list[i:i+3] for i in range(0, len(user_list), 3)]
    table = Table(data, colWidths=[160] * 3)
    style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
    table.setStyle(style)
    pdf.build([table])
    return pdf_name

def DEF_CONVERT_TO_SECEND(MESSAGE_TEXT):
    TIME, UNIT = MESSAGE_TEXT.split()
    TIME = int(TIME)
    if UNIT == 'min':
        return TIME * 60
    elif UNIT == 'hour':
        return TIME * 3600
    elif UNIT == 'day':
        return TIME * 86400
    else:
        return None
    
def DEF_USERS_TIME_LIST (CHATID , CATAGORY , TIME) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/users"
    RESPONCE = requests.get(url=URL, headers=PANEL_TOKEN)
    if RESPONCE.status_code == 200:
        RESPONCE_DATA = RESPONCE.json()
        USERS_LIST = []
        NOT_USER_LIST = []
        for USER in RESPONCE_DATA["users"] :
            USER_TIME = USER.get(CATAGORY)
            if USER_TIME :
                DELTA = (DEF_PATCH_TO_SECEND(USER_TIME)).total_seconds()
                USER_USERNAME = USER.get('username')
                if int(DELTA) <= int(TIME) :
                    USERS_LIST.append(USER_USERNAME)
                else :
                    NOT_USER_LIST.append(USER_USERNAME)
        USERS_LIST.sort()
        NOT_USER_LIST.sort()
    else :
        USERS_LIST = []
        NOT_USER_LIST = []
    return USERS_LIST , NOT_USER_LIST
