#!/bin/bash

cd /app

if [[ "$SSL_RESPONSE" == "y" ]]; then
    DOMAIN="https://$PANEL_DOMAIN"
else
    DOMAIN="http://$PANEL_DOMAIN"
fi

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

INSERT INTO messages (chatid, status) VALUES ('$CHATID', 'off');
INSERT INTO users (chatid, role, name, username, password, domain, step) VALUES ('$CHATID', 'boss', '$NAME', '$PANEL_USER', '$PANEL_PASSWORD', '$DOMAIN', 'None');
INSERT INTO monitoring (chatid, status, check_normal, check_error) VALUES ('$CHATID', 'on', '10', '100');
INSERT INTO bot (chatid, token) VALUES ("$CHATID", "$TOKEN");
EOF

chmod +x monitoring.py
chmod +x holder.py
chmod +x expired.py
chmod +x limiteder.py
chmod +x restart.sh

nohup python3 monitoring.py & disown
nohup python3 holder.py & disown
nohup python3 expired.py & disown
nohup python3 limiteder.py & disown

# Add cronjob
(crontab -l 2>/dev/null; echo "@reboot sleep 20 && /bin/bash /app/restart.sh") | crontab -

echo "Holderbot is running!"
