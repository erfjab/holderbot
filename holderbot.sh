#!/bin/bash

clear && echo -e "\n\n\n      Start installing the Holderbot!     \n\n\n\n\n\n" && sleep 3

clear && echo -e "\n      Checking update and upgrade packages....\n\n" && yes '-' | head -n 50 | tr -d '\n\n' && echo && sleep 1 && apt update && apt upgrade -y || { echo -e "\n\nFailed to update and upgrade packages. Exiting...\n\n"; exit 1; }

clear && echo -e "\n      Checking required packages....\n\n" && yes '-' | head -n 50 | tr -d '\n\n' && echo && sleep 1 && apt install python3 python3-pip git python3-dev python3-venv build-essential libsqlite3-dev -y || { echo -e "\n\nFailed to install required packages. Exiting...\n\n"; exit 1; }

clear && echo -e "\n      Checking directories...      \n\n" && yes '-' | head -n 50 | tr -d '\n\n' && echo

directories=("holderbot" "holderbeta" "holder")
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "Removing existing $dir directory...\n"
        rm -rf "$dir"
    fi
done

clear && echo -e "\n      Checking processes...      \n\n" && yes '-' | head -n 50 | tr -d '\n\n' && echo

processes=("python3 holder.py" "python3 holderbeta.py" "python3 node_status_checker.py" "python3 monitoringbeta.py" "python3 monitoring.py" "python3 expired.py" "python3 limiteder.py")
for proc in "${processes[@]}"; do
    if ps aux | grep -v grep | grep "$proc" &> /dev/null; then
        proc_name=$(echo "$proc" | cut -d ' ' -f 2)
        echo -e "Stopping existing $proc_name process...\n"
        pkill -f "$proc"
    fi
done

clear && echo -e "\n      Checking hold venv...      \n\n" && yes '-' | head -n 50 | tr -d '\n\n' && echo

mkdir -p holderbot && cd holderbot && git clone -b main https://github.com/erfjab/holderbot.git .
python3 -m venv hold && source hold/bin/activate

clear && echo -e "\n      Checking python library...      \n\n" && yes '-' | head -n 50 | tr -d '\n\n' && echo

pip install -U pyrogram tgcrypto requests Pillow qrcode[pil] persiantools pytz python-dateutil pysqlite3 cdifflib reportlab && \
sudo apt-get install -y sqlite3

while true; do
    clear && echo -e "\n      Complete the information.      \n\n" && yes '-' | head -n 50 | tr -d '\n\n' && echo
    
    name=""
    while [[ -z "$name" || ! "$name" =~ ^[a-zA-Z]+$ ]]; do
        read -p "Please enter name (nickname) : " name
        if [[ -z "$name" ]]; then
            echo "Name cannot be empty. Please enter a valid name."
        elif [[ ! "$name" =~ ^[a-zA-Z]+$ ]]; then
            echo "Name must contain only English letters. Please enter a valid name."
        fi
    done

    chatid=""
    while [[ ! "$chatid" =~ ^[0-9]+$ ]]; do
        read -p "Please enter telegram chatid : " chatid
        if [[ ! "$chatid" =~ ^[0-9]+$ ]]; then
            echo "Chat ID must be a number. Please enter a valid number."
        fi
    done

    token=""
    while [[ -z "$token" || ! "$token" =~ ^[0-9]+:.+$ ]]; do
        read -p "Please enter telegram bot token: " token
        if [[ ! "$token" =~ ^[0-9]+:.+$ ]]; then
            echo "Invalid token format. Please enter a valid token."
        else
            response=$(curl -s "https://api.telegram.org/bot$token/getMe")
            if [[ "$response" != *"ok\":true"* ]]; then
                echo "Invalid token. Please enter a valid token."
                token=""
            fi
        fi
    done

    user=""
    while [[ -z "$user" ]]; do
        read -p "Please enter panel sudo username : " user
        if [[ -z "$user" ]]; then
            echo "Username cannot be empty. Please enter a valid username."
        fi
    done

    password=""
    while [[ -z "$password" ]]; do
        read -p "Please enter panel sudo password : " password
        if [[ -z "$password" ]]; then
            echo "Password cannot be empty. Please enter a valid password."
        fi
    done

    domain_simple=""
    while [[ ! "$domain_simple" =~ ^[a-zA-Z0-9.-]+\:[0-9]+$ ]]; do
        read -p "Please enter panel domain (like: sub.domain.com:port) : " domain_simple
        if [[ ! "$domain_simple" =~ ^[a-zA-Z0-9.-]+\:[0-9]+$ ]]; then
            echo "Invalid domain format. Please enter a valid domain in the format sub.domain.com:port."
        fi
    done

    ssl_response=""
    while [[ ! "$ssl_response" =~ ^[ynYN]$ ]]; do
        read -p "Do you have SSL? (y/n): " ssl_response
        if [[ ! "$ssl_response" =~ ^[ynYN]$ ]]; then
            echo "Please enter 'y' for Yes or 'n' for No."
        fi
    done

    if [[ $ssl_response == "y" || $ssl_response == "Y" ]]; then
        domain="https://$domain_simple"
    else
        domain="http://$domain_simple"
    fi

    clear && echo -e "\n      Checking information...      \n\n" && yes '-' | head -n 50 | tr -d '\n\n' && echo
    echo "Name: $name"
    echo "Telegram Chat ID: $chatid"
    echo "Telegram Bot Token: $token"
    echo "Panel Sudo Username: $user"
    echo "Panel Sudo Password: $password"
    echo "Panel Domain: $domain"

    read -p "Are these information correct? (y/n): " correct
    if [[ $correct == "y" || $correct == "Y" ]]; then
        clear && echo -e "\n      Checking panel...      \n\n" && printf "%0.s-" {1..50} && echo && sleep 1
        response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -d "username=$user&password=$password" "$domain/api/admin/token")
        if [[ $response -eq 200 ]]; then
            echo "Authentication successful." && sleep 1
            break
        else
            echo "Authentication failed. Please check your information and try again." && sleep 2
        fi
    fi
done

clear && echo -e "\n      Creating database...      \n\n" && yes '-' | head -n 50 | tr -d '\n\n' && echo

while true; do
    sqlite3 holder.db <<EOF
CREATE TABLE IF NOT EXISTS bot
    (chatid INTEGER PRIMARY KEY,
     token TEXT);

CREATE TABLE IF NOT EXISTS monitoring
    (chatid INTEGER PRIMARY KEY,
     status TEXT,
     check_normal INTEGER,
     check_error INTEGER);

CREATE TABLE IF NOT EXISTS templates
    (name TEXT PRIMARY KEY,
     data INTEGER,
     date INTEGER,
     proxies TEXT,
     inbounds TEXT);

CREATE TABLE IF NOT EXISTS users
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
INSERT INTO bot (chatid, token) VALUES ('$chatid', '$token');
EOF

    if [[ $? -eq 0 ]]; then
        echo "Database setup successful."
        break
    else
        echo "Error: Database setup failed. Retrying..."
    fi
done

clear && echo -e "\n      Running the bot...      \n\n" && yes '-' | head -n 50 | tr -d '\n\n' && echo

count=0
while true; do
    chmod +x monitoring.py holder.py expired.py limiteder.py restart.sh
    nohup python3 monitoring.py & disown
    nohup python3 holder.py & disown
    nohup python3 expired.py & disown
    nohup python3 limiteder.py & disown
    sleep 1
    echo -e "\n\nplease wait...\n\n"
    sleep 7

    if ! pgrep -x "monitoring.py" && ! pgrep -x "holder.py" && ! pgrep -x "expired.py" && ! pgrep -x "limiteder.py"; then
        echo "Scripts are running successfully."
        break
    else
        ((count++))
        if (( count > 3 )); then
            echo "Error: Scripts could not be started after multiple attempts."
            exit 1
        fi
        echo "Scripts are still running. Retrying..."
    fi
done

crontab -l | grep -vF "/bin/bash /holderbot/restart.sh" | crontab -
cronjob="@reboot sleep 20 && /bin/bash /holderbot/restart.sh"
if ! crontab -l | grep -Fq "$cronjob" >/dev/null 2>&1; then
  (crontab -l 2>/dev/null; echo "$cronjob") | crontab -
fi

clear && echo -e "\n      Holderbot is run, Enjoy! \n        You can find us in telegram with @ErfJabHolderbot" && yes '-' | head -n 50 | tr -d '\n\n' && echo && sleep 2
