from pyrogram import *      
from pyrogram.types import *
from pyrogram.errors.exceptions import *
from io import *
import json

#------------------------- IMPORT INFO -------------------------#

with open('config.json', 'r') as file:
    CONFIG = json.load(file)

ADMIN_TGBOT = int(CONFIG['admin_telegram_bot'])
PANEL_USER = CONFIG['marzban_panel_username']
PANEL_PASS = CONFIG['marzban_panel_password']
PANEL_DOMAIN = CONFIG['marzban_panel_domain']
TOKEN_TGBOT = CONFIG['telegram_bot_token']

#------------------------- SET BOT  -------------------------#
plugins = dict(root="plugins")
app = Client(   
    "holderbot",      
    api_id=26410400,
    api_hash="408bf51732560cb81a0e32533b858cbf",
    bot_token=TOKEN_TGBOT,
    plugins=plugins)
    
#--------------------------------- RUN INFITY BOT ---------------------------------
app.run()
