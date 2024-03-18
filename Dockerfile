FROM python:3.10

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    build-essential \
    git \
 && rm -rf /var/lib/apt/lists/*

# Clone your project
RUN git clone -b main https://github.com/dry-stan/holderbot .

# Set environment variables
ENV NAME=<YourName>
ENV CHATID=<YourChatID>
ENV TOKEN=<YourToken>
ENV PANEL_USER=<YourPanelUser>
ENV PANEL_PASSWORD=<YourPanelPassword>
ENV PANEL_DOMAIN=<YourPanelDomain>
ENV SSL_RESPONSE=<YourSSLResponse>

# Install Python dependencies
RUN pip install -U pyrogram tgcrypto requests Pillow qrcode[pil] persiantools pytz python-dateutil pysqlite3 cdifflib reportlab

# Install SQLite3
RUN apt-get update && apt-get install -y sqlite3

# Run your script
CMD ["bash", "installation_script.sh"]
