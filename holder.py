from pyrogram import *      
from pyrogram.types import *
from pyrogram.errors.exceptions import *
from io import *
import json , sqlite3

#------------------------- IMPORT INFO -------------------------#
conn = sqlite3.connect('holder.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM config ORDER BY id DESC LIMIT 1")
row = cursor.fetchone()
if row:
    ADMIN_TGBOT = int(row[1])
    PANEL_USER = row[2]
    PANEL_PASS = row[3]
    PANEL_DOMAIN = row[4]
    TOKEN_TGBOT = row[5]
else:
    print("No configuration found in the database. Exiting.")
    exit()
conn.close()

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
