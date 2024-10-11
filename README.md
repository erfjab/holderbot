## 1. Server Setup

### 1.1: Update the Server

Ensure your server is up to date:

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2: Install Docker

Install Docker using this command:

```bash
curl -fsSL https://get.docker.com | sh
```

---

## 2. Download and Configure

### 2.1: Create Directory and Download `docker-compose.yml`

Create the necessary directory and download the `docker-compose.yml` file:

```bash
mkdir -p /opt/erfjab/holderbot/data
curl -o /opt/erfjab/holderbot/docker-compose.yml https://raw.githubusercontent.com/erfjab/holderbot/master/docker-compose.yml
cd /opt/erfjab/holderbot
```

### 2.2: Download and Configure `.env`

Download the example environment file:

```bash
curl -o .env https://raw.githubusercontent.com/erfjab/holderbot/master/.env.example
```

Edit the `.env` file to add your **Telegram Bot Token** and **API keys**:

```bash
nano .env
```

---

## 3. Run the Bot

### 3.1: Pull the Latest Docker Image

Pull the latest Docker image for the bot:

```bash
docker compose pull
```

### 3.2: Start the Bot

Start the bot in detached mode:

```bash
docker compose up -d
```

### 3.3: Verify the Bot is Running

Check the status of running containers:

```bash
docker compose ps
```

---

## Updating the Bot

To update the bot to the latest version:

1. Pull the latest Docker image:

    ```bash
    docker compose pull
    ```

2. Restart the bot:

    ```bash
    docker compose up -d
    ```

---

## Managing the Bot with Docker

### Restart the Bot

```bash
docker compose restart
```

### Stop the Bot

```bash
docker compose down
```

### View Real-Time Logs

```bash
docker compose logs -f
```

---

## Contact & Support

- Telegram Channel: [@ErfJabs](https://t.me/ErfJabs)

Feel free to ⭐ the project to show your support!

[![Stargazers over time](https://starchart.cc/erfjab/holderbot.svg?variant=adaptive)](https://starchart.cc/erfjab/holderbot)