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
TOKEN_TGBOT = CONFIG['telegram_bot_token']

#------------------------- SET BOT  -------------------------#

app = Client(   
    "Noderbot",      
    api_id=26410400,
    api_hash="408bf51732560cb81a0e32533b858cbf",
    bot_token=TOKEN_TGBOT)

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
    
#------------------------------------- ALL DEFS -------------------------------------#

with app :
    while True :

        # set panel info
        PANEL_HEADERS = CREATE_TOKEN_TO_ACCESS_PANEL(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)            

        # set problem timer
        NODE_HAVE_A_PROBLEM = False
        
        # set url
        URL = f"https://{PANEL_DOMAIN}/api/nodes"
        RESPONCE = requests.get(url=URL , headers=PANEL_HEADERS)
        if RESPONCE.status_code == 200 :
            RESPONCE_DATA = RESPONCE.json()

            # check node
            for NODE in RESPONCE_DATA :
                
                # node status
                RD_NODE_STATUS = NODE.get("status")

                if RD_NODE_STATUS == "error" or RD_NODE_STATUS == "connecting" :
                    
                    # node info
                    RD_NODE_NAME = NODE.get("name")
                    RD_NODE_MESSAGE = NODE.get("message")
                    RD_NODE_ADDRESS = NODE.get("address")
                    RD_NODE_ID = NODE.get("id")

                    # set text
                    TEXT = f"<b>🚨مشکلی در یکی از نود های سرورتون پیدا شده! هرچه زودتر بررسی کنید. برای مزاحم نشدن به بررسی شما ، بات تا 2 دقیقه آینده نودهارو چک نخواهد کرد.\n\nسرور نود :</b> {RD_NODE_NAME}\n<b>آیپی نود : </b>{RD_NODE_ADDRESS}\n<b>وضعیت نود : </b>{RD_NODE_STATUS}\n<b>پیام پنل : </b>\n{RD_NODE_MESSAGE}"
                    
                    # set wait more
                    NODE_HAVE_A_PROBLEM = True

                    # send admin
                    app.send_message(chat_id=ADMIN_TGBOT , text=TEXT , parse_mode=enums.ParseMode.HTML)

            # wait next check           
            if NODE_HAVE_A_PROBLEM == True :
                time.sleep(120)        
            else :
                time.sleep(10)

