#!/bin/bash
HOME=/
pkill -f monitoring.py 
pkill -f holder.py 
pkill -f expired.py 
pkill -f limiteder.py 
cd
cd /holderbot
source hold/bin/activate
chmod +x monitoring.py
chmod +x holder.py
chmod +x expired.py
chmod +x limiteder.py
nohup python3 monitoring.py & disown
nohup python3 holder.py & disown
nohup python3 expired.py & disown
nohup python3 limiteder.py & disown