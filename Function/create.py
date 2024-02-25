from Function.db import *
import requests , re


def DEF_GET_INBOUNDS(CHATID) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/inbounds"
    RESPONCE = requests.get(url=URL, headers=PANEL_TOKEN)
    if RESPONCE.status_code == 200:
        RESPONCE_DATA = RESPONCE.json()
        INBOUNDS = json.loads(RESPONCE.text)
        INBOUNDS_ALL = []
        INBOUNDS_SELECT = {}
        for group, ITEMS in RESPONCE_DATA.items():
            for ITEM in ITEMS:
                TAG = ITEM.get('tag')
                if TAG:
                    INBOUNDS_ALL.append(TAG)
                    INBOUNDS_SELECT[TAG] = True       
    else :
        INBOUNDS = {}
        INBOUNDS_ALL = []
        INBOUNDS_SELECT = {}
    return INBOUNDS , INBOUNDS_ALL ,INBOUNDS_SELECT


def DEF_SELECT_INBOUNDS_AND_PROXIES(INBOUNDS , SELECTS) :
    INBOUNDS_ALL = {}
    PROXIES = {}
    for CATAGORY, ITEMS in INBOUNDS.items():
        TAGS = [ITEM['tag'] for ITEM in ITEMS if SELECTS.get(ITEM['tag'], True)]
        if TAGS:
            INBOUNDS_ALL[CATAGORY] = TAGS
            PROXIES[CATAGORY] = {}
    return INBOUNDS_ALL , PROXIES

def DEF_CREATE_USER(CHATID , USERNAME , DATA , DATE , PROXIES , INBOUNDS) :
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    DATA_TO_BYTES = int(float(DATA)*(1024**3))
    DATE_TO_SECOND = int(DATE) * (24*60*60) 
    DATA = {
        "username": USERNAME,
        "proxies": PROXIES,
        "inbounds": INBOUNDS,
        "data_limit": DATA_TO_BYTES,
        "data_limit_reset_strategy": "no_reset",
        "status": "on_hold",
        "note": "by holderbot",
        "on_hold_timeout": "2024-11-03T20:30:00",
        "on_hold_expire_duration": DATE_TO_SECOND} 
    URL = f"https://{PANEL_DOMAIN}/api/user"
    POST_DATA = json.dumps(DATA)
    RESPONCE = requests.post(url=URL , headers=PANEL_TOKEN , data=POST_DATA)
    if RESPONCE.status_code == 200 :
        URL = f"https://{PANEL_DOMAIN}/api/user/{USERNAME}"
        RESPONCE = requests.get(url=URL , headers=PANEL_TOKEN)
        if RESPONCE.status_code == 200 :
            RESPONCE_DATA = json.loads(RESPONCE.text)
            TEXT = RESPONCE_DATA.get("subscription_url")
        else :
            TEXT = f"❌<b> I can't find user.</b>\n<pre>{RESPONCE.text}</pre>"
    else :
        TEXT = f"❌<b> I can't create user.</b>\n<pre>{RESPONCE.text}</pre>"
    return TEXT


def DEF_USERNAME_STARTER(TEXT , MUCH_NUMBER):
    LETTERS = re.findall(r'[a-zA-Z]+', TEXT)
    DIGIT = re.findall(r'\d+', TEXT)
    if LETTERS and not DIGIT:
        START_NUMBER = 1
        RESULT = ''.join(LETTERS) + str(START_NUMBER)
    elif DIGIT and not LETTERS:
        START_NUMBER = int(DIGIT[0])
        RESULT = ''.join(LETTERS) + str(START_NUMBER)
    else:
        START_NUMBER = int(DIGIT[0])
        RESULT = ''.join(LETTERS) + str(START_NUMBER)
    RESULT_LIST = [RESULT]
    for _ in range(int(MUCH_NUMBER) - 1 ):
        START_NUMBER += 1
        RESULT_LIST.append(''.join(LETTERS) + str(START_NUMBER))
    return RESULT_LIST