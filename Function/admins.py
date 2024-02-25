from Function.db import *
import requests , json



def DEF_CHANGE_PASSWORD(CHATID , ADMIN_NAME , ADMIN_SUDO , ADMIN_PASSWORD):
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    ADMIN_SUDO = ADMIN_SUDO == "SUDO"
    URL = f"https://{PANEL_DOMAIN}/api/admin/{ADMIN_NAME}"
    DATA = {"password" : ADMIN_PASSWORD , "is_sudo": ADMIN_SUDO}
    DATA = json.dumps(DATA)
    RESPONCE = requests.put(url=URL, headers=PANEL_TOKEN ,data=DATA)
    if RESPONCE.status_code == 200:
        TEXT = "<b>✅ Admin password is changed.</b>"
    else :
        TEXT = f"<b>❌ I can't change admin password.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    return TEXT

def DEF_CHANGE_SUDO(CHATID , ADMIN_USERNAME , ADMIN_SUDO , ADMIN_PASSWORD) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/admin/{ADMIN_USERNAME}"  
    ADMIN_SUDO = not (ADMIN_SUDO == "SUDO")
    DATA = {"password" : ADMIN_PASSWORD , "is_sudo": ADMIN_SUDO}
    DATA = json.dumps(DATA)
    RESPONCE = requests.put(url=URL, headers=PANEL_TOKEN ,data=DATA)
    if RESPONCE.status_code == 200:
        TEXT = "<b>✅ Admin sudo is changed.</b>"
    else :
        TEXT = f"❌ I can't change admin sudo.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    return TEXT

def DEF_DELETE_ADMIN(CHATID,ADMIN_USERNAME) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/admin/{ADMIN_USERNAME}"        
    RESPONCE = requests.delete(url=URL, headers=PANEL_TOKEN)
    if RESPONCE.status_code == 200:
        TEXT = "<b>✅ Admin is deleted.</b>"
    else :
        TEXT = f"<b>❌ I can't deleted admin.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    return TEXT

def DEF_ADD_ADMIN(CHATID,ADMIN_USERNAME,ADMIN_PASSWORD,ADMIN_SUDO) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/admin"
    DATA = {"username": ADMIN_USERNAME,"is_sudo": ADMIN_SUDO,"password": ADMIN_PASSWORD}
    DATA = json.dumps(DATA)
    RESPONCE = requests.post(url=URL, headers=PANEL_TOKEN ,data=DATA)
    if RESPONCE.status_code == 200:
        TEXT = "<b>✅ Admin is added.</b>"
    else :
        TEXT = f"<b>❌ I can't add admin.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    return TEXT