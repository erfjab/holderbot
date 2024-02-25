import requests , re , pytz
from Function.db import *
from persiantools.jdatetime import JalaliDateTime
from difflib import SequenceMatcher
from datetime import datetime, timezone
from pyrogram.types import *


def DEF_SUB_LINK_FIND_FROM_USER_MESSAGE (LINK) :
    PATTERN = r"([^/]+)"
    MATCH = re.search(PATTERN , LINK)
    if MATCH :
        TOKEN = MATCH.group(1)
        return TOKEN
    else :
        return False
    
def DEF_CONVERT_DIFFERNCE_TIME_TO_REMAINING (DELTA) :
    DAYS = DELTA.days
    HOURS , remainder = divmod(DELTA.seconds , 3600)
    MINUTES, SECONDS = divmod(remainder,60)
    if DAYS > 0 :
        return f"{DAYS} day"
    elif HOURS > 0 :
        return f"{HOURS} hours"
    elif MINUTES > 0 :
        return f"{MINUTES} mintue"
    else :
        return f"{SECONDS} second"

def DEF_PATCH_TO_SECEND(TIME) :
    ONLINE_PATCH = "%Y-%m-%dT%H:%M:%S.%f" if '.' in TIME else "%Y-%m-%dT%H:%M:%S"
    TIME = datetime.strptime(TIME , ONLINE_PATCH )
    TIME_UTC = pytz.utc.localize(TIME)
    TIME_LOCAL = TIME_UTC.astimezone(pytz.timezone('Asia/Tehran'))
    TIME_NOW = datetime.now(pytz.timezone('Asia/Tehran'))
    DELTA = TIME_NOW - TIME_LOCAL
    return DELTA

def DEF_KEYBOARD_UPDATE_STASE(RD_USERNAME) :
    KEYBOARD_UPDATE_STASE = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Update", callback_data=f'user info UPDATE {RD_USERNAME}'),
        InlineKeyboardButton("🖼 QRcode", callback_data=f'user info QRCODE {RD_USERNAME}')],
        [InlineKeyboardButton("🗑 DELETE", callback_data=f'user info DELETE {RD_USERNAME}')]])
    return KEYBOARD_UPDATE_STASE

def DEF_STASE_USER (CHATID , MESSAGE_TEXT , KEYBOARD_HOME):
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    SUB_LINK_FINDER = re.findall(r'https://[^/]+/sub/([^/]+)', MESSAGE_TEXT)
    if SUB_LINK_FINDER :
        SUB_TOKEN = DEF_SUB_LINK_FIND_FROM_USER_MESSAGE(SUB_LINK_FINDER[0])
        URL = f"https://{PANEL_DOMAIN}/sub/{SUB_TOKEN}/info"
    else :
        URL = f"https://{PANEL_DOMAIN}/api/user/{MESSAGE_TEXT}"
    RESPONCE = requests.get(url=URL , headers=PANEL_TOKEN)
    if RESPONCE.status_code == 200 :
        RESPONCE_DATA = json.loads(RESPONCE.text)
    else :
        URL = f"https://{PANEL_DOMAIN}/api/users"
        RESPONCE = requests.get(url=URL , headers=PANEL_TOKEN)
        if RESPONCE.status_code == 200 :
            RESPONCE_DATA = RESPONCE.json()
            USERS = [user.get('username').lower() for user in RESPONCE_DATA.get('users', [])]
            similarity_scores = [(user, SequenceMatcher(None, MESSAGE_TEXT.lower(), user).ratio()) for user in USERS]
            similar_users = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            similar_users = [user for user, score in similar_users if score > 0.55]
            if similar_users:
                similar_users_text = " <b>|</b> ".join([f"<code>{user}</code>" for user in similar_users])
                TEXT = f"<b>Did you mean :</b> {similar_users_text}"
            else :
                TEXT = "<b>I can't find user.</b>"
        else :
            TEXT = "<b>I can't find user.</b>"
        return TEXT , KEYBOARD_HOME
    RD_USERNAME = RESPONCE_DATA.get("username")
    RD_STATUS = RESPONCE_DATA.get("status")           
    if RD_STATUS == "active" or RD_STATUS == "expired" or RD_STATUS == "limited" or RD_STATUS == "disabled" :
        RD_DATE = RESPONCE_DATA.get("expire")
        if RD_DATE :
            RD_DATE_JALALI = JalaliDateTime.utcfromtimestamp(RD_DATE).strftime("%Y/%m/%d")
            UTC_TIME = datetime.utcfromtimestamp(RD_DATE).replace(tzinfo=timezone.utc)
            TIME_REMAINING = UTC_TIME - (datetime.now(timezone.utc))
            RD_DATE_LEFT = DEF_CONVERT_DIFFERNCE_TIME_TO_REMAINING(TIME_REMAINING)
            if RD_STATUS == "expired" :
                RD_DATE_LEFT = "❌"
        else :
            RD_DATE_JALALI = None
            RD_DATE_LEFT = "♾"
        RD_DATA_USED = round((RESPONCE_DATA.get("used_traffic")) / (1024 ** 3) , 3)
        if RD_STATUS == "limited" :
            RD_DATA_USED = "❌"
        RD_DATA_LIMIT = RESPONCE_DATA.get("data_limit")
        if RD_DATA_LIMIT :
            RD_DATA_LIMIT = round((RESPONCE_DATA.get("data_limit")) / (1024 ** 3) , 3)
        else :
            RD_DATA_LIMIT = "♾"
        if RESPONCE_DATA.get("online_at") :
            RD_LAST_ONLINE = f"{DEF_CONVERT_DIFFERNCE_TIME_TO_REMAINING(DEF_PATCH_TO_SECEND(RESPONCE_DATA.get('online_at')))} ago"
        else : 
            RD_LAST_ONLINE = "➖"
        if RESPONCE_DATA.get("sub_updated_at") :
            RD_SUB_LAST_UPDATE = f"{DEF_CONVERT_DIFFERNCE_TIME_TO_REMAINING(DEF_PATCH_TO_SECEND(RESPONCE_DATA.get('sub_updated_at')))} ago"
        else : 
            RD_SUB_LAST_UPDATE = "➖"
        RD_USER_AGENT = RESPONCE_DATA.get("sub_last_user_agent")
        if not RD_USER_AGENT :
            RD_USER_AGENT = "➖"
        TEXT = f"<b>Username :</b> {RD_USERNAME} ({RD_STATUS})\n"
        TEXT += f"<b>Data Used :</b> {RD_DATA_USED} GB ({RD_DATA_LIMIT} GB)\n"
        TEXT += f"<b>Date Left :</b> {RD_DATE_LEFT}\n"
        if RD_DATE_JALALI :
            TEXT += f"<b>Expiration Date :</b> {RD_DATE_JALALI}\n"
        TEXT += f"<b>App Used :</b> {RD_USER_AGENT}\n"
        TEXT += f"<b>Last online time :</b> {RD_LAST_ONLINE}\n"
        TEXT += f"<b>Last update sub :</b> {RD_SUB_LAST_UPDATE}\n"
    elif RD_STATUS == "on_hold" :
        RD_ON_HOLD_DATE = int((RESPONCE_DATA.get("on_hold_expire_duration")) / (24*60*60))
        RD_ON_HOLD_DATA = int((RESPONCE_DATA.get("data_limit")) / (1024 ** 3))
        RD_ON_HOLD_DATA_USERS = "limited"
        TEXT = f"<b>Username :</b> {RD_USERNAME} ({RD_STATUS})\n<b>Data {RD_ON_HOLD_DATA_USERS} :</b> {RD_ON_HOLD_DATA} GB\n<b>Date {RD_ON_HOLD_DATA_USERS} :</b> {RD_ON_HOLD_DATE} Days"
    KEYBOARD_UPDATE_STASE = DEF_KEYBOARD_UPDATE_STASE(RD_USERNAME)
    return TEXT , KEYBOARD_UPDATE_STASE