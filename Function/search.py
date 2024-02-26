from Function.db import *
from difflib import SequenceMatcher
import requests


def DEF_SEARCH_USERS (CHATID , MESSAGE_TEXT):
    PANEL_USER, PANEL_PASS, PANEL_DOMAIN = DEF_IMPORT_DATA (CHATID)
    PANEL_TOKEN = DEF_PANEL_ACCESS(PANEL_USER, PANEL_PASS, PANEL_DOMAIN)
    URL = f"https://{PANEL_DOMAIN}/api/users"
    RESPONCE = requests.get(url=URL , headers=PANEL_TOKEN)
    if RESPONCE.status_code == 200 :
        RESPONCE_DATA = RESPONCE.json()
        USERS = [user.get('username') for user in RESPONCE_DATA.get('users', [])]
        similarity_scores = [(user, SequenceMatcher(None, MESSAGE_TEXT, user).ratio()) for user in USERS]
        similar_users = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similar_users = [user for user, score in similar_users if score > 0.55]
        if similar_users:
            similar_users_text = "<b>,</b> ".join([f"<code>{user}</code>" for user in similar_users])
            TEXT = f"<b>Did you mean?</b> {similar_users_text}\n\n<b>❕Return to the home page to receive user statistics.</b>"
        else :
            TEXT = f"<b>❌ I can't find any user.</b>"
    else :
        TEXT = f"<b>❌ I can't check users.</b>\n<pre>{str(RESPONCE.text)}</pre>"
    return TEXT
