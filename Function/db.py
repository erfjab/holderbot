import sqlite3 , requests , json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def DEF_GET_BOT_TOKEN():
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT token FROM bot''')
    second_column_value = cursor.fetchone()[0] 
    conn.close()
    return second_column_value

def DEF_CHECK_BOSS(CHATID):
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE chatid=?", (CHATID,))
    USER_STEP = cursor.fetchone()
    conn.close()
    if USER_STEP and USER_STEP[0] == "boss":
        return True
    else:
        return False

def DEF_CHECK_STEP(CHATID) :
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute("SELECT step FROM users WHERE chatid=?", (CHATID,))
    USER_STEP = cursor.fetchone()
    conn.close()
    return USER_STEP[0]

def DEF_UPDATE_STEP(CHATID,NEW_STEP) :
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET step=? WHERE chatid=?", (NEW_STEP, CHATID,))
    conn.commit()
    conn.close()

def DEF_IMPORT_DATA (CHATID) :
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, domain FROM users WHERE chatid=?", (CHATID,))
    USER_INFO = cursor.fetchone()
    conn.close()
    return USER_INFO

def DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN) :
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
        return False

def DEF_MONITORING_DATA():
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM monitoring''')
    USER_DATA = cursor.fetchone()
    conn.close()
    return USER_DATA

def DEF_CHANGE_NODE_STATUS(CHATID , STATUS) :
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE monitoring SET status = ? WHERE chatid = ?", (STATUS, CHATID))
    conn.commit()
    conn.close()

def DEF_NODE_STATUS(CHATID , ROW , STATUS) :
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE monitoring SET {ROW} = ? WHERE chatid = ?", (STATUS, CHATID))
    conn.commit()
    conn.close()

def DEF_TEMPLATES_DATA():
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, data, date FROM templates")
    USER_DATA = cursor.fetchall()
    conn.close()
    return USER_DATA
    
def DEF_TEMPLATES_DELETE(TEM_NAME) :
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM templates WHERE name = ?", (TEM_NAME,))
    conn.commit()
    conn.close()

def DEF_TEMPLATES_ADD(NAME, DATA, DATE, PROXIES, INBOUNDS):
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO templates (name, data, date, proxies, inbounds) VALUES (?, ?, ?, ?, ?)",
                   (NAME, DATA, DATE, json.dumps(PROXIES), json.dumps(INBOUNDS)))
    conn.commit()
    conn.close()

def DEF_CHECK_TEMPLATES_NAME(TEXT):
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM templates WHERE name = ?", (TEXT,))
    result = cursor.fetchone()    
    conn.close()
    return result is not None

def DEF_TEMPLATES_DATA_ALL(TEXT):
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM templates WHERE name = ?", (TEXT,))
    result = cursor.fetchone()    
    conn.close()
    return result

def DEF_MESSAGER_IMPORT_DATA():
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM messages''')
    USER_DATA = cursor.fetchone()
    conn.close()
    return USER_DATA

def DEF_GET_MESSAGE_STATUS(CHATID):
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT status FROM messages WHERE chatid = ?''', (CHATID,))
    USER_DATA = cursor.fetchone()
    conn.close()
    if USER_DATA:
        return USER_DATA[0]
    else:
        return None

def DEF_CHANGE_MESSAGER_STATUS(CHATID):
    OLD_STATUS = DEF_GET_MESSAGE_STATUS(CHATID)
    conn = sqlite3.connect('holder.db')
    cursor = conn.cursor()
    if OLD_STATUS == "on" :    
        cursor.execute('''UPDATE messages SET status = ? WHERE chatid = ?''', ("off", CHATID))
        conn.commit()
        conn.close()
        TEXT = "<b>✅ Your status is off.</b>"
    else :
        PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
        PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
        URL = f"https://{PANEL_DOMAIN}/api/inbounds"
        RESPONCE = requests.get(url=URL, headers=PANEL_TOKEN , verify=False)
        if RESPONCE.status_code == 200:
            INBOUNDS = json.loads(RESPONCE.text)
            FOUND = False
            if "shadowsocks" in INBOUNDS :
                for ITEM in INBOUNDS["shadowsocks"]:
                    if "Holderbot" in ITEM["tag"]:
                        FOUND = True
                        break
            else :
                FOUND = False
            if FOUND :
                cursor.execute('''UPDATE messages SET status = ? WHERE chatid = ?''', ("on", CHATID))
                conn.commit()
                conn.close()
                TEXT = "<b>✅ Your status is on.</b>"
            else :
                TEXT = "<b>❌ Your status is not change.\nyou don't have Holderbot inbounds!</b>"
        else :
            TEXT = "<b>❌ i can't check inbounds!</b>"
    return TEXT
