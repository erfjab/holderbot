from pyrogram import *      
from pyrogram.types import *
from pyrogram.errors.exceptions import *
from io import *
import json

#------------------------- IMPORT INFO -------------------------#
with open('config.json', 'r', encoding='latin-1') as file:
    config = json.load(file)

telegram_bot_token = config['telegram_bot_token']

#------------------------- SET BOT  -------------------------#
plugins = dict(root="plugins")
app = Client(   
    "holderbot",      
    api_id=26410400,
    api_hash="408bf51732560cb81a0e32533b858cbf",
    bot_token=telegram_bot_token,
    plugins=plugins)
    
#--------------------------------- RUN INFITY BOT ---------------------------------
app.run()
