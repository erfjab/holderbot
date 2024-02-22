#!/bin/bash

cd && cd ..

sudo apt-get update
sudo apt-get install -y python3-dev
sudo apt-get install -y libsqlite3-dev

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


if ps aux | grep -v grep | grep "python3 monitoringbeta.py" &> /dev/null; then
    echo "Stopping existing holderbot process..."
    pkill -f "python3 monitoringbeta.py"
fi

if ps aux | grep -v grep | grep "python3 holderbeta.py" &> /dev/null; then
    echo "Stopping existing holder process..."
    pkill -f "python3 holderbeta.py"
fi

pkill -x "python3 holderbeta.py"

if [ -d "holderbeta" ]; then
    echo "Removing existing holderbeta directory..."
    rm -rf holderbeta
fi

mkdir holderbeta
cd holderbeta

git clone -b beta https://github.com/erfjab/holderbot.git .

sudo apt install -y python3.10-venv
python3 -m venv hold
source hold/bin/activate

pip install -U pyrogram tgcrypto requests Pillow qrcode[pil] persiantools pytz python-dateutil pysqlite3 cdifflib reportlab

read -p "Please enter telegram chatid : " chatid
read -p "Please enter name (nickname) : " name
read -p "Please enter panel username : " user
read -p "Please enter panel password : " password
read -p "Please enter panel domain (like : sub.domian.com:port ) : " domain
read -p "Please enter telegram bot token: " token

# Create SQLite database
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

INSERT INTO users (chatid, role, name, username, password, domain, step) VALUES ('$chatid', 'boss', '$name', '$user', '$password', '$domain', 'None');
INSERT INTO monitoring (chatid, status, check_normal, check_error) VALUES ('$chatid', 'on', '10', '100');
INSERT INTO bot (chatid, token) VALUES ("$chatid", "$token");
EOF

chmod +x monitoringbeta.py
chmod +x holderbeta.py
nohup python3 monitoringbeta.py & disown
nohup python3 holderbeta.py & disown
