from pyrogram import *
from pyrogram.types import *
from pyrogram.errors.exceptions import *
from datetime import datetime, timezone
from persiantools.jdatetime import JalaliDateTime
from io import *
from dateutil import tz
import requests , json , time , qrcode , html , re , pytz

#------------------------------------- JSON INFO -------------------------------------#

with open('config.json', 'r') as file:
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
    
#------------------------------------- ON MESSAGE & FIVE LEN MESSAGE -------------------------------------#

@Client.on_message(filters.private & filters.command("cr") & filters.user(ADMIN_TGBOT))
async def create(client: Client, message: Message) :
    CHATID = message.chat.id
    try :
        
        # get message text and id
        MESSAGES = message.text

        # split message 
        MESSAGES_SPLIT = MESSAGES.strip().split(" ")
        if len(MESSAGES_SPLIT) == 6 and MESSAGES_SPLIT[2].isnumeric() and MESSAGES_SPLIT[3].isnumeric() and (MESSAGES_SPLIT[4].isnumeric() or MESSAGES_SPLIT[4].lower() == "unlimited") and MESSAGES_SPLIT[5].isnumeric() :


            # set users info 
            global USER_TAG , USER_START , USER_HOW , USER_DATA , USER_DATE
            USER_TAG = MESSAGES_SPLIT[1]
            USER_START = int(MESSAGES_SPLIT[2])
            USER_HOW = int(MESSAGES_SPLIT[3])
            USER_DATA = MESSAGES_SPLIT[4]
            USER_DATE = int(MESSAGES_SPLIT[5])
            
            # set confirm text
            TEXT = f"<b>اسم کاربر : </b>{USER_TAG}\n<b>استارت از : </b>{USER_START}\n<b>تعداد کاربر : </b>{USER_HOW}\n<b>محدودیت حجم : </b>{USER_DATA} گیگ\n<b>محدودیت زمان : </b>{USER_DATE} روز"

            # set keyboard
            KEYBOARD = InlineKeyboardMarkup([
                [InlineKeyboardButton("بله, بساز", callback_data='cryesshowinbounds'),
                InlineKeyboardButton("بیخیال", callback_data='cr no')]])
            
            # send message
            await client.send_message(chat_id=ADMIN_TGBOT , text=TEXT , parse_mode=enums.ParseMode.HTML ,reply_markup=KEYBOARD)

            # set panel info
            PANEL_HEADERS = CREATE_TOKEN_TO_ACCESS_PANEL(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)            

            # set inbounds url
            URL = f"https://{PANEL_DOMAIN}/api/inbounds"
            RESPONCE = requests.get(url=URL, headers=PANEL_HEADERS)
            if RESPONCE.status_code == 200:
                RESPONCE_DATA = RESPONCE.json()
            else :
                ERROR_MESSAGE = f"<b>❌ ارور در چک اینباند:</b>\n<code>{RESPONCE.text}</code>"
                await client.send_message(chat_id=CHATID, text=ERROR_MESSAGE, parse_mode=enums.ParseMode.HTML)     
                return
                       
            global INBOUNDS_TAG_ALL , INBOUNDS_TAG_NAME
            INBOUNDS_TAG_ALL = []
            INBOUNDS_TAG_NAME = {}

            for group, ITEMS in RESPONCE_DATA.items():
                for ITEM in ITEMS:
                    TAG = ITEM.get('tag')
                    if TAG:
                        INBOUNDS_TAG_ALL.append(TAG)
                        INBOUNDS_TAG_NAME[TAG] = True 
                                    
    except Exception as e :
        ERROR_MESSAGE = f"<b>❌ ارور :</b>\n<code>{str(e)}</code>"
        await client.send_message(chat_id=CHATID, text=ERROR_MESSAGE, parse_mode=enums.ParseMode.HTML) 


@Client.on_callback_query(filters.regex(r'^cr'))
async def handle_callback_create(client: Client, query: CallbackQuery):
    CHATID = query.message.chat.id
    try :

        # set panel info
        PANEL_HEADERS = CREATE_TOKEN_TO_ACCESS_PANEL(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)            
        
        # set callback data
        CALLBACK_DATA = query.data

        # set globals
        global INBOUNDS_TAG_ALL , INBOUNDS_TAG_NAME , USER_TAG , USER_START , USER_HOW , USER_DATA , USER_DATE

        # set keyboard select
        KEYBOARD_SELECT = "➕"
        KEYBOARD_NOT_SELECT = "➖"
        
        if CALLBACK_DATA == "cryesshowinbounds" :
            KEYBOARD_COLUMNS = 2
            KEYBOARD_ROWS = (len(INBOUNDS_TAG_ALL) + KEYBOARD_COLUMNS - 1) // KEYBOARD_COLUMNS
            KEYBOARD_INBOUNDS = [
                [InlineKeyboardButton(f"{KEYBOARD_SELECT} {TAG}", callback_data=f"cr tag {TAG}") for TAG in INBOUNDS_TAG_ALL[KEYBOARD_ROWS * KEYBOARD_COLUMNS:(KEYBOARD_ROWS + 1) * KEYBOARD_COLUMNS]]
                for KEYBOARD_ROWS in range(KEYBOARD_ROWS)
            ]
            KEYBOARD_INBOUNDS.append([
                InlineKeyboardButton("❌ بیخیال", callback_data="cr no"),
                InlineKeyboardButton("✅ برو بعدی", callback_data="cr createusers")
            ])
            await query.edit_message_text(text="<b>لطفا اینباندهای مدنظرتون رو انتخاب کنید.</b>" , reply_markup=InlineKeyboardMarkup(KEYBOARD_INBOUNDS) , parse_mode=enums.ParseMode.HTML)

        elif CALLBACK_DATA.startswith("cr tag") :
            SELECTED_TAG = CALLBACK_DATA[7:]
            INBOUNDS_TAG_NAME[SELECTED_TAG] = not INBOUNDS_TAG_NAME[SELECTED_TAG]
            KEYBOARD_COLUMNS = 2
            KEYBOARD_ROWS = (len(INBOUNDS_TAG_ALL) + KEYBOARD_COLUMNS - 1) // KEYBOARD_COLUMNS
            KEYBOARD_INBOUNDS = [
                [InlineKeyboardButton(f"{KEYBOARD_SELECT if INBOUNDS_TAG_NAME[TAG] else KEYBOARD_NOT_SELECT} {TAG}", callback_data=f"cr tag {TAG}") for TAG in INBOUNDS_TAG_ALL[KEYBOARD_ROWS * KEYBOARD_COLUMNS:(KEYBOARD_ROWS + 1) * KEYBOARD_COLUMNS]]
                for KEYBOARD_ROWS in range(KEYBOARD_ROWS)
            ]
            KEYBOARD_INBOUNDS.append([
                InlineKeyboardButton("❌ بیخیال", callback_data="cr no"),
                InlineKeyboardButton("✅ بسازش", callback_data="cr createusers")
            ])
            await query.edit_message_text(text="<b>لطفا اینباندهای مدنظرتون رو انتخاب کنید.</b>" , reply_markup=InlineKeyboardMarkup(KEYBOARD_INBOUNDS) , parse_mode=enums.ParseMode.HTML)

        elif CALLBACK_DATA == "cr createusers" :

            # set inbounds url
            URL = f"https://{PANEL_DOMAIN}/api/inbounds"
            RESPONCE = requests.get(url=URL, headers=PANEL_HEADERS)
            if RESPONCE.status_code == 200:
                RESPONCE_DATA = RESPONCE.json()
            else :
                ERROR_MESSAGE = f"<b>❌ ارور در چک اینباند:</b>\n<code>{RESPONCE.text}</code>"
                await client.send_message(chat_id=CHATID, text=ERROR_MESSAGE, parse_mode=enums.ParseMode.HTML)     
                return
            
            # set inbounds
            FORMATTED_DATA = {}
            for CATAGORY , ITEMS in RESPONCE_DATA.items() :
                FORMATTED_DATA[CATAGORY] = [ITEM["tag"] for ITEM in ITEMS ]
            
            # set True selected inbounds
            for CATAGORY , TAGS in FORMATTED_DATA.items() :
                FORMATTED_DATA[CATAGORY] = [TAG for TAG in TAGS if INBOUNDS_TAG_NAME.get(TAG , True)]

            # set empty catagory inbounds
            FORMATTED_DATA = {CATAGORY: TAGS for CATAGORY, TAGS in FORMATTED_DATA.items() if TAGS}

            if not FORMATTED_DATA :
                await query.answer(text="<b>خب همه شو که حذف کردی ، الان با چی کانفیگ بسازیم؟</b>")
                return
            else :
                await query.delete.message()
            
            # set proxys
            PROXY_LIST = {}
            for CATAGORY , TAGS in FORMATTED_DATA.items() :
                PROXY_LIST[CATAGORY] = {}
            
            # set data
            if USER_DATA.lower() == "unlimited" :
                DATA_TO_BYTE = 0
            else :
                DATA_TO_BYTE = int(USER_DATA)*(1024**3)
            
            # set date
            DATE_TO_SECOND = USER_DATE * (24*60*60)

            # set number for stop
            STOP_NUMBER = 0

            while True :
                
                # set username
                USER_NAME = f"{USER_TAG}{USER_START}"

                # set url data for post
                DATA={
                "username": USER_NAME,
                "proxies" : PROXY_LIST,
                "inbounds": FORMATTED_DATA,
                "expire" : 0,
                "data_limit": DATA_TO_BYTE,
                "data_limit_reset_strategy": "no_reset",
                "status": "on_hold",
                "note": "",
                "on_hold_timeout": "2024-11-03T20:30:00",
                "on_hold_expire_duration": DATE_TO_SECOND
                }          

                URL = f"https://{PANEL_DOMAIN}/api/user"
                POST_DATA = json.dumps(DATA)
                RESPONCE = requests.post(url=URL , headers=PANEL_HEADERS , data=POST_DATA)
                if RESPONCE.status_code == 200 :

                    # set get url 
                    URL = f"https://{PANEL_DOMAIN}/api/user/{USER_NAME}"
                    RESPONCE = requests.get(url=URL , headers=PANEL_HEADERS)
                    if RESPONCE.status_code == 200 :
                        RESPONCE_DATA = json.loads(RESPONCE.text)
                        RD_SUB_URL = RESPONCE_DATA.get("subscription_url")
                        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=10,
                            border=4,
                        )
                        qr.add_data(RD_SUB_URL)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")
                        img_bytes_io = BytesIO()
                        qr_img.save(img_bytes_io, 'PNG')
                        img_bytes_io.seek(0)
                        await client.send_photo(chat_id=ADMIN_TGBOT , photo=img_bytes_io,caption=f"<code>{html.escape(RD_SUB_URL)}</code>")
                        await client.send_message(chat_id=ADMIN_TGBOT , text=f"<b>✅ {USER_NAME} | {USER_DATA} GB | {USER_DATE} Days</b>" , parse_mode=enums.ParseMode.HTML) 
                        
                        # set stoper
                        STOP_NUMBER += 1
                        if STOP_NUMBER == USER_HOW :
                            break
                        else :
                            USER_START = USER_START + 1
                        
                    else :
                        TEXT = f"<b>❌ ارور ارسال کاربر</b>\n<code>{str(RESPONCE.text)}</code>"
                        await client.send_message(chat_id=ADMIN_TGBOT , text=TEXT , parse_mode=enums.ParseMode.HTML) 
                        break

                else :
                    TEXT = f"<b>❌ ارور ساخت کاربر</b>\n<code>{str(RESPONCE.text)}</code>"
                    await client.send_message(chat_id=ADMIN_TGBOT , text=TEXT , parse_mode=enums.ParseMode.HTML) 
                    break
        elif CALLBACK_DATA == "cr no" :
            await query.edit_message_text(text="<b>باشه رئیس ، بیخیال شدیم...</b>" , parse_mode=enums.ParseMode.HTML)


    except Exception as e :
        ERROR_MESSAGE = f"<b>❌ ارور :</b>\n<code>{str(e)}</code>"
        await query.edit_message_text(text=ERROR_MESSAGE, parse_mode=enums.ParseMode.HTML) 
        return
