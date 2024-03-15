#!/bin/bash

cd && cd ..

sudo apt-get update
sudo apt-get install -y python3-dev
sudo apt-get install -y libsqlite3-dev
sudo apt install build-essential

if ! command -v python3 &> /dev/null; then
    echo "Python not found. Installing..."
    sudo apt-get install -y python3
fi

if ! command -v git &> /dev/null; then
    echo "Git not found. Installing..."
    sudo apt-get install -y git
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found. Installing..."
    sudo apt-get install -y python3-pip
fi

if [ -d "holderbot" ]; then
    echo "Removing existing holderbeta directory..."
    rm -rf holderbot
fi

if [ -d "holderbeta" ]; then
    echo "Removing existing holderbeta directory..."
    rm -rf holderbeta
fi

if [ -d "holder" ]; then
    echo "Removing existing holder directory..."
    rm -rf holder
fi

if ps aux | grep -v grep | grep "python3 holder.py" &> /dev/null; then
    echo "Stopping existing holder process..."
    pkill -f "python3 holder.py"
fi

if ps aux | grep -v grep | grep "python3 holderbeta.py" &> /dev/null; then
    echo "Stopping existing holder process..."
    pkill -f "python3 holderbeta.py"
fi

if ps aux | grep -v grep | grep "python3 node_status_checker.py" &> /dev/null; then
    echo "Stopping existing node_status_checker process..."
    pkill -f "python3 node_status_checker.py"
fi

if ps aux | grep -v grep | grep "python3 monitoringbeta.py" &> /dev/null; then
    echo "Stopping existing monitoringbeta process..."
    pkill -f "python3 monitoringbeta.py"
fi

if ps aux | grep -v grep | grep "python3 monitoring.py" &> /dev/null; then
    echo "Stopping existing monitoring process..."
    pkill -f "python3 monitoring.py"
fi

if ps aux | grep -v grep | grep "python3 expired.py" &> /dev/null; then
    echo "Stopping existing expired process..."
    pkill -f "python3 expired.py"
fi

if ps aux | grep -v grep | grep "python3 limiteder.py" &> /dev/null; then
    echo "Stopping existing limiteder process..."
    pkill -f "python3 limiteder.py"
fi

mkdir holderbot
cd holderbot

git clone -b main https://github.com/erfjab/holderbot.git .

sudo apt install -y python3.10-venv
python3 -m venv hold
source hold/bin/activate

pip install -U pyrogram tgcrypto requests Pillow qrcode[pil] persiantools pytz python-dateutil pysqlite3 cdifflib reportlab
sudo apt-get install sqlite3

read -p "Please enter name (nickname) : " name
read -p "Please enter telegram chatid : " chatid
read -p "Please enter telegram bot token: " token
read -p "Please enter panel sudo username : " user
read -p "Please enter panel sudo password : " password
read -p "Please enter panel domain (like: sub.domian.com:port) : " domain

sqlite3 holder.db <<EOF
CREATE TABLE bot
    (chatid INTEGER PRIMARY KEY,
     token TEXT);

CREATE TABLE monitoring
    (chatid INTEGER PRIMARY KEY,
     status TEXT,
     check_normal INTEGER,
     check_error INTEGER);

CREATE TABLE templates
    (name TEXT PRIMARY KEY,
     data INTEGER,
     date INTEGER,
     proxies TEXT,
     inbounds TEXT);

CREATE TABLE users
    (chatid INTEGER PRIMARY KEY,
     role TEXT,
     name TEXT,
     username TEXT,
     password TEXT,
     domain TEXT,
     step TEXT);

CREATE TABLE IF NOT EXISTS messages
    (chatid INTEGER PRIMARY KEY,
    status TEXT);

INSERT INTO messages (chatid, status) VALUES ('$chatid', 'off');
INSERT INTO users (chatid, role, name, username, password, domain, step) VALUES ('$chatid', 'boss', '$name', '$user', '$password', '$domain', 'None');
INSERT INTO monitoring (chatid, status, check_normal, check_error) VALUES ('$chatid', 'on', '10', '100');
INSERT INTO bot (chatid, token) VALUES ("$chatid", "$token");
EOF

chmod +x monitoring.py
chmod +x holder.py
chmod +x expired.py
chmod +x limiteder.py
nohup python3 monitoring.py & disown
nohup python3 holder.py & disown
nohup python3 expired.py & disown
nohup python3 limiteder.py & disown
chmod +x restart.sh
cronjob="@reboot sleep 20 && /bin/bash /holderbot/restart.sh"
if ! crontab -l | grep -Fq "$cronjob"; then
  (crontab -l 2>/dev/null; echo "$cronjob") | crontab -
fi
