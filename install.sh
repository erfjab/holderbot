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

# ایجاد پوشه holderbot
mkdir holderbot
cd holderbot

# دریافت اسکریپت از GitHub
git clone https://github.com/erfjab/holderbot.git .

# نصب پیش‌نیازها
pip3 install -r requirements.txt
pip install -U pyrogram tgcrypto
# اجرای اسکریپت اصلی
python3 holderbot.py
