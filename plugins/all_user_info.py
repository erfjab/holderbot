from pyrogram import *
from pyrogram.types import *
from pyrogram.errors.exceptions import *
from datetime import datetime, timezone
from persiantools.jdatetime import JalaliDateTime
from io import *
from dateutil import tz
import requests , json , time , qrcode , html , re , pytz

#------------------------------------- JSON INFO -------------------------------------#

with open('config.json', 'r', encoding='latin-1') as file:
    CONFIG = json.load(file)

ADMIN_TGBOT = int(CONFIG['admin_telegram_bot'])
PANEL_USER = CONFIG['marzban_panel_username']
PANEL_PASS = CONFIG['marzban_panel_password']
PANEL_DOMAIN = CONFIG['marzban_panel_domain']

#------------------------------------- ALL DEFS -------------------------------------#

def CREATE_TOKEN_TO_ACCESS_PANEL (PANEL_USER , PANEL_PASS , PANEL_DOMAIN) :
    PANEL_TOKEN_DATA = {"username" : PANEL_USER , "password" : PANEL_PASS }
    PANEL_TOKEN = requests.post(url=f"https://{PANEL_DOMAIN}/api/admin/token" , data=PANEL_TOKEN_DATA)
    if PANEL_TOKEN.status_code == 200 :
        PANEL_TOKEN_BACK = json.loads(PANEL_TOKEN.text)
        PANEL_HEADERS = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': f"Bearer {PANEL_TOKEN_BACK.get('access_token')}"}
        return PANEL_HEADERS
    else :
        return None

def CHECK_STATUS_USERS ( RESPONCE_DATA , CHECK_STATUS ) :
    LEN_USERS = 0
    LIST_USERS = []
    for USER in RESPONCE_DATA.get("users") :
        USER_STATUS = USER.get("status")
        USER_USERNAME = USER.get("username")
        if CHECK_STATUS == "on_hold" :
            USER_LAST_TIME = USER.get("online_at")
            if USER_LAST_TIME == None :
                LEN_USERS += 1
                LIST_USERS.append(USER_USERNAME)
        else :
            if USER_STATUS == CHECK_STATUS :
                LIST_USERS.append(USER_USERNAME)
                LEN_USERS += 1
    LIST_USERS.sort()
    return LEN_USERS , LIST_USERS

def CHECK_LAST_TIME_ONLINE_USERS ( RESPONCE_DATA , CHECK_TIME , TIME_TO_CHECK) :
    LEN_USERS = 0
    LIST_USERS = []
    for USER in RESPONCE_DATA.get("users") :
        USER_LAST_TIME = USER.get("online_at")
        if USER_LAST_TIME :
            USER_USERNAME = USER.get("username")
            ONLINE_PATCH = "%Y-%m-%dT%H:%M:%S.%f" if '.' in USER_LAST_TIME else "%Y-%m-%dT%H:%M:%S"
            USER_LAST_TIME = datetime.strptime(USER_LAST_TIME , ONLINE_PATCH )
            ONLINE_TIME_UTC = pytz.utc.localize(USER_LAST_TIME)
            ONLINE_TIME_LOCAL = ONLINE_TIME_UTC.astimezone(pytz.timezone('Asia/Tehran'))
            TIME_NOW = datetime.now(pytz.timezone('Asia/Tehran'))
            DELTA = TIME_NOW - ONLINE_TIME_LOCAL
            if CHECK_TIME == "online" :
                if DELTA.total_seconds() <= int(TIME_TO_CHECK) :
                    LIST_USERS.append(USER_USERNAME)
                    LEN_USERS += 1
            else :
                if DELTA.total_seconds() > int(TIME_TO_CHECK) :
                    LIST_USERS.append(USER_USERNAME)
                    LEN_USERS += 1
    LIST_USERS.sort()
    return LEN_USERS , LIST_USERS            

#------------------------------------- ON MESSAGE & LIST MESSAGE -------------------------------------#

@Client.on_message(filters.private & filters.command("users") & filters.user(ADMIN_TGBOT))
async def ONE_USER_INFO (client: Client, message: Message) :
    CHATID = message.chat.id
    try :

        # set panel info
        PANEL_HEADERS = CREATE_TOKEN_TO_ACCESS_PANEL(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)            

        # set url
        URL = f"https://{PANEL_DOMAIN}/api/users"
        RESPONCE = requests.get(url=URL , headers=PANEL_HEADERS)
        if RESPONCE.status_code == 200 :
            RESPONCE_DATA = json.loads(RESPONCE.text)

            # get len and list users
            RD_LEN_ALL_USERS = RESPONCE_DATA.get("total")
            RD_LEN_ACTIVE_USERS , RD_LIST_ACTIVE_USERS = CHECK_STATUS_USERS(RESPONCE_DATA,"active")
            RD_LEN_DISABLED_USERS , RD_LIST_DISABLED_USERS = CHECK_STATUS_USERS(RESPONCE_DATA,"disabled")
            RD_LEN_EXPIRED_USERS , RD_LIST_EXPIRED_USERS = CHECK_STATUS_USERS(RESPONCE_DATA,"expired")
            RD_LEN_LIMITED_USERS , RD_LIST_LIMITED_USERS = CHECK_STATUS_USERS(RESPONCE_DATA,"limited")
            RD_LEN_ON_HOLD_USERS , RD_LIST_ON_HOLD_USERS = CHECK_STATUS_USERS(RESPONCE_DATA,"on_hold")
            RD_LEN_ONLINES_USERS , RD_LIST_ONLINES_USERS = CHECK_LAST_TIME_ONLINE_USERS(RESPONCE_DATA,"online",86400)
            RD_LEN_OFFLINES_USERS , RD_LIST_OFFLINES_USERS = CHECK_LAST_TIME_ONLINE_USERS(RESPONCE_DATA,"offline",86400)

            # set text
            TEXT = f"""
<b>کل کاربران :</b> {RD_LEN_ALL_USERS}
<b>کاربران فعال :</b> {RD_LEN_ACTIVE_USERS}
<b>کاربران غیرفعال :</b> {RD_LEN_DISABLED_USERS}
<b>کاربران اتمام زمان :</b> {RD_LEN_EXPIRED_USERS}
<b>کاربران اتمام حجم :</b> {RD_LEN_LIMITED_USERS}
<b>کاربران استارت نخورده :</b> {RD_LEN_ON_HOLD_USERS}
<b>کاربران آنلاین در 24 ساعت اخیر :</b> {RD_LEN_ONLINES_USERS}
<b>کاربران آفلاین بیش از 24 ساعت :</b> {RD_LEN_OFFLINES_USERS}

<b>برای دریافت لیست کاربر مدنظرتون میتوانید از کیبوردهای زیر استفاده کنید.</b>
"""
            
            #set keyboard
            KEYBOARD_BUTTONS = [
                [
                    InlineKeyboardButton("کاربران فعال", callback_data="list_active_users"),
                    InlineKeyboardButton("کاربران غیرفعال", callback_data="list_disabled_users")
                ],
                [
                    InlineKeyboardButton("کاربران اتمام حجم", callback_data="list_limited_users"),
                    InlineKeyboardButton("کاربران اتمام زمان", callback_data="list_expired_users")
                ],
                [
                    InlineKeyboardButton("کاربران آنلاین", callback_data="list_online_users"),
                    InlineKeyboardButton("کاربران آفلاین", callback_data="list_offline_users")
                ],
                [
                    InlineKeyboardButton("کاربران استارت نخورده", callback_data="list_on_hold_users")
                ]
            ]
            KEYBOARD = InlineKeyboardMarkup(KEYBOARD_BUTTONS)
            
            # send message
            await client.send_message(chat_id=CHATID , text=TEXT , reply_markup=KEYBOARD , parse_mode=enums.ParseMode.HTML)
            return


        else :
            await client.send_message(chat_id=CHATID , text=f"<b>❌ ارور در بررسی یوزرها :</b> \n<code>{RESPONCE.text}</code>" , parse_mode=enums.ParseMode.HTML)                
            return
    
    except Exception as e :
        ERROR_MESSAGE = f"<b>❌ ارور :</b>\n<code>{str(e)}</code>"
        await client.send_message(chat_id=CHATID, text=ERROR_MESSAGE, parse_mode=enums.ParseMode.HTML) 


@Client.on_callback_query(filters.regex(r'^list'))
async def handle_callback_all_user(client: Client, query: CallbackQuery):
    CHATID = query.message.chat.id
    try :

        # set callback
        CALLBACK_DATA = query.data
        if CALLBACK_DATA.startswith("list_") :

            # set panel info
            PANEL_HEADERS = CREATE_TOKEN_TO_ACCESS_PANEL(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)            

            # set url
            URL = f"https://{PANEL_DOMAIN}/api/users"
            RESPONCE = requests.get(url=URL , headers=PANEL_HEADERS)
            if RESPONCE.status_code == 200 :
                RESPONCE_DATA = json.loads(RESPONCE.text)

                # get len and list users
                RD_LEN_ALL_USERS = RESPONCE_DATA.get("total")
                RD_LEN_ACTIVE_USERS , RD_LIST_ACTIVE_USERS = CHECK_STATUS_USERS(RESPONCE_DATA,"active")
                RD_LEN_DISABLED_USERS , RD_LIST_DISABLED_USERS = CHECK_STATUS_USERS(RESPONCE_DATA,"disabled")
                RD_LEN_EXPIRED_USERS , RD_LIST_EXPIRED_USERS = CHECK_STATUS_USERS(RESPONCE_DATA,"expired")
                RD_LEN_LIMITED_USERS , RD_LIST_LIMITED_USERS = CHECK_STATUS_USERS(RESPONCE_DATA,"limited")
                RD_LEN_ON_HOLD_USERS , RD_LIST_ON_HOLD_USERS = CHECK_STATUS_USERS(RESPONCE_DATA,"on_hold")
                RD_LEN_ONLINES_USERS , RD_LIST_ONLINES_USERS = CHECK_LAST_TIME_ONLINE_USERS(RESPONCE_DATA,"online",86400)
                RD_LEN_OFFLINES_USERS , RD_LIST_OFFLINES_USERS = CHECK_LAST_TIME_ONLINE_USERS(RESPONCE_DATA,"offline",86400)

                # set list
                if CALLBACK_DATA == "list_active_users" :
                    CB_LIST = RD_LIST_ACTIVE_USERS
                    CB_LEN = RD_LEN_ACTIVE_USERS
                    CB_NAME = "لیست کاربران فعال"
                elif CALLBACK_DATA == "list_disabled_users" :
                    CB_LIST = RD_LIST_DISABLED_USERS
                    CB_LEN = RD_LEN_DISABLED_USERS
                    CB_NAME = "لیست کاربران غیرفعال"
                elif CALLBACK_DATA == "list_expired_users" :
                    CB_LIST = RD_LIST_EXPIRED_USERS
                    CB_LEN = RD_LEN_EXPIRED_USERS
                    CB_NAME = "لیست کاربران اتمام زمان"
                elif CALLBACK_DATA == "list_limited_users" :
                    CB_LIST = RD_LIST_LIMITED_USERS
                    CB_LEN = RD_LEN_LIMITED_USERS
                    CB_NAME = "لیست کاربران اتمام حجم"
                elif CALLBACK_DATA == "list_on_hold_users" :
                    CB_LIST = RD_LIST_ON_HOLD_USERS
                    CB_LEN = RD_LEN_ON_HOLD_USERS
                    CB_NAME = "لیست کاربران استارت نخورده"
                elif CALLBACK_DATA == "list_online_users" :
                    CB_LIST = RD_LIST_ONLINES_USERS
                    CB_LEN = RD_LEN_ONLINES_USERS
                    CB_NAME = "لیست کاربران آنلاین"
                elif CALLBACK_DATA == "list_offline_users" :
                    CB_LIST = RD_LIST_OFFLINES_USERS
                    CB_LEN = RD_LEN_OFFLINES_USERS
                    CB_NAME = "لیست کاربران آفلاین"

                # check list None
                if CB_LIST == [] :
                    await query.answer(text="هیچ کاربری در لیست انتخابی موجود نمی باشد")
                    return
                
                # send message
                LEN_SEND = 0
                LEN_ALL_USERS = int(CB_LEN)
                TEXT = f"<b>{CB_NAME} :</b>\n\n"
                for USER in CB_LIST :
                    TEXT += f"<code>{USER}</code>   "
                    LEN_SEND += 1
                    if LEN_SEND == 99 or LEN_SEND == LEN_ALL_USERS :
                        await client.send_message(chat_id=ADMIN_TGBOT , text=TEXT , parse_mode=enums.ParseMode.HTML)
                        LEN_SEND = 0
                        LEN_ALL_USERS -= 99
                        TEXT = f"<b>{CB_NAME}</b> :\n\n"

            else :
                await client.send_message(chat_id=CHATID , text=f"<b>❌ ارور در بررسی یوزرها :</b> \n<code>{RESPONCE.text}</code>" , parse_mode=enums.ParseMode.HTML)                
                return
        else :
            pass

    except Exception as e :
        ERROR_MESSAGE = f"<b>❌ ارور :</b>\n<code>{str(e)}</code>"
        await client.send_message(chat_id=CHATID, text=ERROR_MESSAGE, parse_mode=enums.ParseMode.HTML) 

