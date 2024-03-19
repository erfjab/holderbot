from pyrogram import *
from Function.db import *
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

app = Client( 
    "limiteder",      
    api_id=26410400,
    api_hash="408bf51732560cb81a0e32533b858cbf",
    bot_token=DEF_GET_BOT_TOKEN())

with app :
    while True :
        try :
            BOSS_CHATID , STATUS = DEF_MESSAGER_IMPORT_DATA()
            if STATUS == "on" :
                PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (BOSS_CHATID)
                PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
                URL = f"{PANEL_DOMAIN}/api/users?status=limited"
                RESPONCE = requests.get(url=URL , headers=PANEL_TOKEN , verify=False)
                
                if RESPONCE.status_code == 200 :
                    RESPONCE_DATA = RESPONCE.json()
                    for USER in RESPONCE_DATA["users"] :
                        if not USER["inbounds"] == {'shadowsocks': ['Holderbot']} :
                            USERNAME = USER["username"]
                            URL = f"{PANEL_DOMAIN}/api/user/{USERNAME}"
                            DATA = {"proxies":{"shadowsocks":{}},"inbounds" : {'shadowsocks': ['Holderbot']}}
                            RESPONCE = requests.put(url=URL , json=DATA , headers=PANEL_TOKEN , verify=False)
                            if RESPONCE.status_code == 200 :
                                app.send_message(chat_id=BOSS_CHATID , text=f"<b>✅ (Checker) Boss! user <code>{USERNAME}</code> is limited,\nI have set the messages.</b>" , parse_mode=enums.ParseMode.HTML , disable_notification=True)
                            else :
                                app.send_message(chat_id=BOSS_CHATID , text=f"<b>❗ (Checker) Boss! user <code>{USERNAME}</code> is limited,\nbut I can't set the messages.\n\n<pre>{RESPONCE.text}</pre></b>" , parse_mode=enums.ParseMode.HTML , disable_notification=True)                                
                        time.sleep(0.5)
                time.sleep(5)
            else :
                time.sleep(60)
        except Exception as e :
            app.send_message(chat_id=BOSS_CHATID , text=f"<b>❌ (Checker) limiteder Error :</b>\n<pre>{str(e)}</pre>" , parse_mode=enums.ParseMode.HTML , disable_notification=True)
            time.sleep(60)
            pass
