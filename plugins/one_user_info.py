from pyrogram import *
from pyrogram.types import *
from pyrogram.errors.exceptions import *
from datetime import datetime, timezone
from persiantools.jdatetime import JalaliDateTime
from io import *
from dateutil import tz
import requests , json , time , qrcode , html , re , pytz

#------------------------------------- JSON INFO -------------------------------------#

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

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


def SUB_LINK_FIND_FROM_USER_MESSAGE (LINK) :
    PATTERN = r"([^/]+)"
    MATCH = re.search(PATTERN , LINK)
    if MATCH :
        TOKEN = MATCH.group(1)
        return TOKEN
    else :
        return False
    
def CONVERT_DIFFERNCE_TIME_TO_REMAINING (DELTA) :
    DAYS = DELTA.days
    HOURS , remainder = divmod(DELTA.seconds , 3600)
    MINUTES, SECONDS = divmod(remainder,60)
    if DAYS > 0 :
        return f"{DAYS} روز"
    elif HOURS > 0 :
        return f"{HOURS} ساعت"
    elif MINUTES > 0 :
        return f"{MINUTES} دقیقه"
    else :
        return f"{SECONDS} ثانیه"

def LAST_TIME_TO_TIME_DIFFERNCE (LAST_TIME) :
    ONLINE_PATCH = "%Y-%m-%dT%H:%M:%S.%f" if '.' in LAST_TIME else "%Y-%m-%dT%H:%M:%S"
    ONLINE_TIME = datetime.strptime(LAST_TIME, ONLINE_PATCH)
    ONLINE_TIME_UTC = pytz.utc.localize(ONLINE_TIME)
    ONLINE_TIME_LOCAL = ONLINE_TIME_UTC.astimezone(pytz.timezone('Asia/Tehran'))
    TIME_NOW = datetime.now(pytz.timezone('Asia/Tehran'))
    DELTA = TIME_NOW - ONLINE_TIME_LOCAL
    CREATE_REMAINING = CONVERT_DIFFERNCE_TIME_TO_REMAINING(DELTA)
    return CREATE_REMAINING

#------------------------------------- ON MESSAGE & ONE LEN MESSAGE -------------------------------------#

@Client.on_message(filters.private & ~filters.command("start") & ~filters.command("users") & ~filters.command("cr"))
async def ONE_USER_INFO (client: Client, message: Message) :
    CHATID = message.chat.id
    try :

        # check text or caption 
        if message.photo :
            MESSAGES = message.caption
        else :
            MESSAGES = message.text
        
        # split message 
        MESSAGES_SPLIT = MESSAGES.strip().split(" ")
        if len(MESSAGES_SPLIT) == 1 and not MESSAGES.startswith("/") :
            
            # set panel info
            PANEL_HEADERS = CREATE_TOKEN_TO_ACCESS_PANEL(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)            
            
            # check name or link and get user info
            SUB_LINK_FINDER =   re.findall(r'https://[^/]+/sub/([^/]+)', MESSAGES)
            if SUB_LINK_FINDER :
                SUB_TOKEN = SUB_LINK_FIND_FROM_USER_MESSAGE(SUB_LINK_FINDER[0])
                URL = f"https://{PANEL_DOMAIN}/sub/{SUB_TOKEN}/info"
                RESPONCE = requests.get(url=URL , headers=PANEL_HEADERS)        
            else : 
                if CHATID == ADMIN_TGBOT :
                    URL = f"https://{PANEL_DOMAIN}/api/user/{MESSAGES}"
                    RESPONCE = requests.get(url=URL , headers=PANEL_HEADERS)
                else :
                    await client.send_message(chat_id=CHATID , text=f"<b>لطفا لینک تون رو ارسال کنید.</b>" , parse_mode=enums.ParseMode.HTML)
                    return
            if RESPONCE.status_code == 200 :

                # loads data
                RESPONCE_DATA = json.loads(RESPONCE.text)
                RD_USERNAME = RESPONCE_DATA.get("username")
                RD_STATUS = RESPONCE_DATA.get("status")

                # check status
                if RD_STATUS == "active" or RD_STATUS == "expired" or RD_STATUS == "limited" or RD_STATUS == "disabled" :
                    if RD_STATUS == "active" :
                        RD_STATUS = "فعال"
                    elif RD_STATUS == "expired" :
                        RD_STATUS = "اتمام زمان"
                    elif RD_STATUS == "limited" :
                        RD_STATUS = "اتمام حجم"
                    elif RD_STATUS == "disabled" :
                        RD_STATUS = "غیرفعال"
                        
                    # set date
                    RD_DATE = RESPONCE_DATA.get("expire")
                    if RD_DATE :
                        RD_DATE_JALALI = JalaliDateTime.utcfromtimestamp(RD_DATE).strftime("%Y/%m/%d")
                        UTC_TIME = datetime.utcfromtimestamp(RD_DATE).replace(tzinfo=timezone.utc)
                        TIME_REMAINING = UTC_TIME - (datetime.now(timezone.utc))
                        RD_DATE_LEFT = CONVERT_DIFFERNCE_TIME_TO_REMAINING(TIME_REMAINING)
                        if RD_STATUS == "اتمام زمان" :
                            RD_DATE_LEFT = "تمام شده"
                    else :
                        RD_DATE_JALALI = None
                        RD_DATE_LEFT = "نامحدود"

                    #set data
                    RD_DATA_USED = round((RESPONCE_DATA.get("used_traffic")) / (1024 ** 3) , 3)
                    RD_DATA_LIMIT = RESPONCE_DATA.get("data_limit")
                    if RD_DATA_LIMIT :
                        RD_DATA_LIMIT = round(RD_DATA_LIMIT / (1024 ** 3) , 3)
                        RD_DATA_LEFT = round(RD_DATA_LIMIT - RD_DATA_USED , 3)
                        RD_DATA_LEFT = f"{RD_DATA_LEFT} گیگ"
                        RD_DATA_LEFT_USERS = "مانده"
                        if RD_STATUS == "اتمام حجم" :
                            RD_DATA_LEFT = "تمام شده"
                    else :
                        RD_DATA_LEFT_USERS = "معرفی"
                        RD_DATA_LEFT = RD_DATA_USED

                    # set online
                    RD_LAST_ONLINE = LAST_TIME_TO_TIME_DIFFERNCE(RESPONCE_DATA.get("online_at"))

                    # set update
                    RD_SUB_LAST_UPDATE = LAST_TIME_TO_TIME_DIFFERNCE(RESPONCE_DATA.get("sub_updated_at"))

                    # set text tgbot
                    TEXT = f"<b>نام کاربری : </b>{RD_USERNAME} ({RD_STATUS})\n<b>حجم {RD_DATA_LEFT_USERS} :</b> {RD_DATA_LEFT}\n<b>روز مانده :</b> {RD_DATE_LEFT}"
                    if RD_DATE_JALALI :
                        TEXT += f"\n<b>تاریخ انقضاء :</b> {RD_DATE_JALALI}"
                    if CHATID == ADMIN_TGBOT :
                        TEXT += f"\n<b>آخرین تایم آنلاینی :</b> {RD_LAST_ONLINE} پیش"
                        TEXT += f"\n<b>آخرین آپدیت ساب :</b> {RD_SUB_LAST_UPDATE} پیش"
                    
                    # set keyboard
                    KEYBOARD = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 بروزرسانی آمار", callback_data=f'info one {RD_USERNAME}')]])

                    # send message
                    await client.send_message(chat_id=CHATID , text=TEXT , reply_markup=KEYBOARD ,  parse_mode=enums.ParseMode.HTML)
                    return
                
                # check status onhold
                elif RD_STATUS == "on_hold" :
                    RD_STATUS = "استارت نخورده"

                    # set date
                    RD_ON_HOLD_DATE = int((RESPONCE_DATA.get("on_hold_expire_duration")) / (24*60*60))

                    # set data
                    RD_ON_HOLD_DATA = int((RESPONCE_DATA.get("data_limit")) / (1024 ** 3))
                    RD_ON_HOLD_DATA_USERS = "تعیین شده"

                    # set text tgbot 
                    TEXT = f"<b>نام کاربری : </b>{RD_USERNAME} ({RD_STATUS})\n<b>حجم {RD_ON_HOLD_DATA_USERS} :</b> {RD_ON_HOLD_DATA} گیگ\n<b>روز تعیین شده :</b> {RD_ON_HOLD_DATE} روز"

                    #set keyboard
                    KEYBOARD = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 بروزرسانی آمار", callback_data=f'reset_stase_{RD_USERNAME}')]])

                    # send message
                    await client.send_message(chat_id=CHATID , text=TEXT , reply_markup=KEYBOARD , parse_mode=enums.ParseMode.HTML)
                    return
                
            else :
                await client.send_message(chat_id=CHATID , text="<b>یوزر پیدا نشد!</b>" , parse_mode=enums.ParseMode.HTML)                
                return
        else :
            pass

    except Exception as e :
        ERROR_MESSAGE = f"<b>❌ ارور :</b>\n<code>{str(e)}</code>"
        await client.send_message(chat_id=CHATID, text=ERROR_MESSAGE, parse_mode=enums.ParseMode.HTML) 

    

@Client.on_callback_query(filters.regex(r'^info one'))
async def handle_callback_one_user(client: Client, query: CallbackQuery):
    CHATID = query.message.chat.id
    try :

        # set callback
        CALLBACK_DATA = query.data

        # set panel info
        PANEL_HEADERS = CREATE_TOKEN_TO_ACCESS_PANEL(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)            

        # set username
        CALLBACK_DATA_SPLIT = CALLBACK_DATA.strip().split(" ")
        CB_USERNAME = CALLBACK_DATA_SPLIT[2]

        URL = f"https://{PANEL_DOMAIN}/api/user/{CB_USERNAME}"
        RESPONCE = requests.get(url=URL , headers=PANEL_HEADERS)
        if RESPONCE.status_code == 200 :

            # loads data
            RESPONCE_DATA = json.loads(RESPONCE.text)
            RD_USERNAME = RESPONCE_DATA.get("username")
            RD_STATUS = RESPONCE_DATA.get("status")

            # check status
            if RD_STATUS == "active" or RD_STATUS == "expired" or RD_STATUS == "limited" or RD_STATUS == "disabled" :
                if RD_STATUS == "active" :
                    RD_STATUS = "فعال"
                elif RD_STATUS == "expired" :
                    RD_STATUS = "اتمام زمان"
                elif RD_STATUS == "limited" :
                    RD_STATUS = "اتمام حجم"
                elif RD_STATUS == "disabled" :
                    RD_STATUS = "غیرفعال"
                    
                # set date
                RD_DATE = RESPONCE_DATA.get("expire")
                if RD_DATE :
                    RD_DATE_JALALI = JalaliDateTime.utcfromtimestamp(RD_DATE).strftime("%Y/%m/%d")
                    UTC_TIME = datetime.utcfromtimestamp(RD_DATE).replace(tzinfo=timezone.utc)
                    TIME_REMAINING = UTC_TIME - (datetime.now(timezone.utc))
                    RD_DATE_LEFT = CONVERT_DIFFERNCE_TIME_TO_REMAINING(TIME_REMAINING)
                    if RD_STATUS == "اتمام زمان" :
                        RD_DATE_LEFT = "تمام شده"
                else :
                    RD_DATE_JALALI = None
                    RD_DATE_LEFT = "نامحدود"

                #set data
                RD_DATA_USED = round((RESPONCE_DATA.get("used_traffic")) / (1024 ** 3) , 3)
                RD_DATA_LIMIT = RESPONCE_DATA.get("data_limit")
                if RD_DATA_LIMIT :
                    RD_DATA_LIMIT = round(RD_DATA_LIMIT / (1024 ** 3) , 3)
                    RD_DATA_LEFT = round(RD_DATA_LIMIT - RD_DATA_USED , 3)
                    RD_DATA_LEFT = f"{RD_DATA_LEFT} گیگ"
                    RD_DATA_LEFT_USERS = "مانده"
                    if RD_STATUS == "اتمام حجم" :
                        RD_DATA_LEFT = "تمام شده"
                else :
                    RD_DATA_LEFT_USERS = "معرفی"
                    RD_DATA_LEFT = RD_DATA_USED

                # set online
                RD_LAST_ONLINE = LAST_TIME_TO_TIME_DIFFERNCE(RESPONCE_DATA.get("online_at"))

                # set update
                RD_SUB_LAST_UPDATE = LAST_TIME_TO_TIME_DIFFERNCE(RESPONCE_DATA.get("sub_updated_at"))

                # set text tgbot
                TEXT = f"<b>نام کاربری : </b>{RD_USERNAME} ({RD_STATUS})\n<b>حجم {RD_DATA_LEFT_USERS} :</b> {RD_DATA_LEFT}\n<b>روز مانده :</b> {RD_DATE_LEFT}"
                if RD_DATE_JALALI :
                    TEXT += f"\n<b>تاریخ انقضاء :</b> {RD_DATE_JALALI}"
                if CHATID == ADMIN_TGBOT :
                    TEXT += f"\n<b>آخرین تایم آنلاینی :</b> {RD_LAST_ONLINE} پیش"
                    TEXT += f"\n<b>آخرین آپدیت ساب :</b> {RD_SUB_LAST_UPDATE} پیش"
                
                # set keyboard
                KEYBOARD = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 بروزرسانی آمار", callback_data=f'info one {RD_USERNAME}')]])

                # send message
                await query.edit_message_text(text=TEXT , reply_markup=KEYBOARD ,  parse_mode=enums.ParseMode.HTML)
                return
            
            # check status onhold
            elif RD_STATUS == "on_hold" :
                RD_STATUS = "استارت نخورده"

                # set date
                RD_ON_HOLD_DATE = int((RESPONCE_DATA.get("on_hold_expire_duration")) / (24*60*60))

                # set data
                RD_ON_HOLD_DATA = int((RESPONCE_DATA.get("data_limit")) / (1024 ** 3))
                RD_ON_HOLD_DATA_USERS = "تعیین شده"

                # set text tgbot 
                TEXT = f"<b>نام کاربری : </b>{RD_USERNAME} ({RD_STATUS})\n<b>حجم {RD_ON_HOLD_DATA_USERS} :</b> {RD_ON_HOLD_DATA} گیگ\n<b>روز تعیین شده :</b> {RD_ON_HOLD_DATE} روز"

                #set keyboard
                KEYBOARD = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 بروزرسانی آمار", callback_data=f'reset_stase_{RD_USERNAME}')]])

                # send message
                await query.edit_message_text(text=TEXT , reply_markup=KEYBOARD , parse_mode=enums.ParseMode.HTML)
                return
            
        else :
            await query.edit_message_text(text="<b>یوزر پیدا نشد!</b>" , parse_mode=enums.ParseMode.HTML)                
            return

    except MessageNotModified :
        await query.answer(text="آمار شما تغییری نکرده.")
        return
    except ValueError :
        ERROR_MESSAGE = f"<b>❌ ارور :</b>\n<code>The day variable must be a number</code>"
        await query.edit_message_text(text=ERROR_MESSAGE, parse_mode=enums.ParseMode.HTML) 
    except Exception as e :
        ERROR_MESSAGE = f"<b>❌ ارور :</b>\n<code>{str(e)}</code>"
        await query.edit_message_text(text=ERROR_MESSAGE, parse_mode=enums.ParseMode.HTML) 
        return
