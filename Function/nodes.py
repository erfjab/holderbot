from Function.db import *
import requests , json



def DEF_STASE_NODE(CHATID  , NODE_ID) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/node/{NODE_ID}"
    RESPONCE = requests.get(url=URL , headers=PANEL_TOKEN)
    if RESPONCE.status_code == 200 :
        RESPONCE_DATA = RESPONCE.json()
        TEXT = f"<b>Node name :</b> {RESPONCE_DATA.get('name')}\n<b>Node status :</b> {RESPONCE_DATA.get('status')}\n<b>Node IP :</b> <code>{RESPONCE_DATA.get('address')}</code>\n<b>Node ID :</b> <code>{RESPONCE_DATA.get('id')}</code>\n<b>usage_coefficient :</b> <code>{RESPONCE_DATA.get('usage_coefficient')}</code>"
    else :
        TEXT = f"<b>❌ I can't check stase node.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    return TEXT

def DEF_RECONNECT_NODE(CHATID , NODE_ID) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/node/{NODE_ID}"
    RESPONCE = requests.get(url=URL , headers=PANEL_TOKEN)
    if RESPONCE.status_code == 200 :
        RESPONCE_DATA = RESPONCE.json()
        if RESPONCE_DATA.get("status") == "disabled" :
            TEXT = "<b>❌ Your node is disabled\nplease first active node.</b>"
        else :
            URL = f"https://{PANEL_DOMAIN}/api/node/{NODE_ID}/reconnect"                
            RESPONCE = requests.post(url=URL , headers=PANEL_TOKEN)
            if RESPONCE.status_code == 200 :
                TEXT = "<b>✅ Your node is reconnected.</b>" 
            else :
                TEXT = f"<b>❌ I can't reconnect node.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    else :
        TEXT = f"<b>❌ I can't check node.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    return TEXT

def DEF_ACTIVE_NODE(CHATID  , NODE_ID) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    NODE_EDIT_DATA = {"status" : "connected"}
    NODE_EDIT_DATA = json.dumps(NODE_EDIT_DATA)
    URL = f"https://{PANEL_DOMAIN}/api/node/{NODE_ID}"
    RESPONCE = requests.put(url=URL , headers=PANEL_TOKEN , data=NODE_EDIT_DATA)
    if RESPONCE.status_code == 200 :
        TEXT = "<b>✅ Your node is active.</b>"
    else :
        TEXT = f"</b>❌ I can't active node.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    return TEXT

def DEF_DISABLED_NODE(CHATID  , NODE_ID) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    NODE_EDIT_DATA = {"status" : "disabled"}
    NODE_EDIT_DATA = json.dumps(NODE_EDIT_DATA)
    URL = f"https://{PANEL_DOMAIN}/api/node/{NODE_ID}"
    RESPONCE = requests.put(url=URL , headers=PANEL_TOKEN , data=NODE_EDIT_DATA)
    if RESPONCE.status_code == 200 :
        TEXT = "<b>✅ Your node is disabled.</b>"
    else :
        TEXT = f"<b>❌ I can't disabled node.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    return TEXT

def DEF_USAGE_COEFFICIENT(USAGE_NUMBER , CHATID , NODE_ID) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    NODE_EDIT_DATA = {"usage_coefficient" : USAGE_NUMBER}
    NODE_EDIT_DATA = json.dumps(NODE_EDIT_DATA)
    URL = f"https://{PANEL_DOMAIN}/api/node/{NODE_ID}"
    RESPONCE = requests.put(url=URL , headers=PANEL_TOKEN , data=NODE_EDIT_DATA)
    if RESPONCE.status_code == 200 :
        TEXT = "<b>✅ Your node usage_coefficient is changed.</b>"
    else :
        TEXT = f"<b>❌ I can't change usage_coefficient.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    return TEXT