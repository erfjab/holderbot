#!/bin/bash

# چک کردن نصب بودن Python، Git و pip3
if ! command -v python3 &> /dev/null; then
    echo "Python not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3
fi

if ! command -v git &> /dev/null; then
    echo "Git not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y git
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# متوقف کردن پروسه holderbot.py اگر در حال اجرا باشد
pkill -x "python3 holderbot.py"
pkill -f "python3 holderbot.py"
pkill -f "python3 holderbot.py"
pkill -f "python3 holderbot.py"

# چک کردن وجود پروسه holderbot.py و قطع کردن آن
if ps aux | grep -v grep | grep "python3 holderbot.py" &> /dev/null; then
    echo "Stopping existing holderbot process..."
    pkill -f "python3 holderbot.py"
fi

# ایجاد پوشه holder
if [ -d "holder" ]; then
    echo "Deleting existing data in holder directory..."
    rm -rf holder
fi

mkdir holder
cd holder

# ایجاد پوشه holderbot
mkdir holderbot
cd holderbot

# از GitHub اسکریپت را دریافت کن
git clone https://github.com/erfjab/holderbot.git .

# ایجاد و فعالسازی محیط مجازی
sudo apt install python3.10-venv
python3 -m venv venv
source venv/bin/activate

# نصب پیش‌نیازها
pip install -r requirements.txt
pip install -U pyrogram tgcrypto

# اطلاعات را از کاربر بخوان
read -p "Please enter admin telegram id: " admin_telegram_bot
read -p "Please enter your telegram bot token: " telegram_bot_token
read -p "Please enter your marzban panel username: " marzban_panel_username
read -p "Please enter your marzban panel password: " marzban_panel_password
read -p "Please enter your marzban panel sub domain name (www.example.com): " marzban_panel_domain

# اطلاعات را در یک فایل JSON بنویس
echo "{
    \"admin_telegram_bot\": $admin_telegram_bot,
    \"telegram_bot_token\": \"$telegram_bot_token\",
    \"marzban_panel_username\": \"$marzban_panel_username\",
    \"marzban_panel_password\": \"$marzban_panel_password\",
    \"marzban_panel_domain\": \"$marzban_panel_domain\"
}" > config.json

chmod +x holderbot.py
nohup python3 holderbot.py
