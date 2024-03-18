from pyrogram import *
from pyrogram.types import *
from pyrogram.errors.exceptions import *
from Function.db import *
import time , requests , json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

app = Client( 
    "noder",      
    api_id=26410400,
    api_hash="408bf51732560cb81a0e32533b858cbf",
    bot_token=DEF_GET_BOT_TOKEN())


with app :

    while True :
        try :
            BOSS_CHATID , NODE_STATUS , CHECK_NORMAL , CHECK_ERROR = DEF_MONITORING_DATA ()
            PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (BOSS_CHATID)
            if NODE_STATUS == "on" :
                
                NODE_HAVE_A_PROBLEM = False
                PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
                URL = f"{PANEL_DOMAIN}/api/nodes"
                RESPONCE = requests.get(url=URL , headers=PANEL_TOKEN , verify=False)
                
                if RESPONCE.status_code == 200 :
                    RESPONCE_DATA = RESPONCE.json()
                    
                    for NODE in RESPONCE_DATA :

                        if NODE.get("status") == "error" or NODE.get("status") == "connecting" :
                            
                            TEXT = f"<b>❗ (Checker) boss of one of the servers crashed. To prevent spamming, server monitoring has been stopped and will be restarted after <code>{CHECK_ERROR}</code> seconds.</b>"
                            TEXT += f"\n\n<b>NODE NAME : </b><code>{NODE.get('name')}</code>\n<b>NODE ID : </b><code>{NODE.get('id')}</code>\n<b>NODE IP : </b><code>{NODE.get('address')}</code>\n<b>ERROR MESSAGE : </b><code>{NODE.get('message')}</code>"
                            NODE_HAVE_A_PROBLEM = True
                            app.send_message(chat_id=BOSS_CHATID , text=TEXT , parse_mode=enums.ParseMode.HTML)

                    if NODE_HAVE_A_PROBLEM is True :
                        time.sleep(int(CHECK_ERROR))        
                    else :
                        time.sleep(int(CHECK_NORMAL))
            
            else :
                time.sleep(60)

        except Exception as e :
            app.send_message(chat_id=BOSS_CHATID , text=f"<b>❌ (Checker) Monitoring Error :</b>\n<pre>{str(e)}</pre>" , parse_mode=enums.ParseMode.HTML)
            time.sleep(60)
            pass
