# ServerManagerBot

**ServerManagerBot** is a Telegram bot designed for managing Hetzner servers. With this bot, administrators can effortlessly control server operations such as listing servers, powering them on or off, rebooting, and resetting passwords—all through Telegram.

## Table of Contents
- [ServerManagerBot](#servermanagerbot)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Getting Started](#getting-started)
    - [1. Setting Up the Server](#1-setting-up-the-server)
      - [Step 1.1: Update the Server](#step-11-update-the-server)
      - [Step 1.2: Install Docker](#step-12-install-docker)
    - [2. Clone the Repository](#2-clone-the-repository)
    - [3. Configure the Bot](#3-configure-the-bot)
      - [Step 3.1: Copy the Example Configuration](#step-31-copy-the-example-configuration)
      - [Step 3.2: Edit the Configuration](#step-32-edit-the-configuration)
    - [4. Docker Setup](#4-docker-setup)
      - [Step 4.1: Docker Compose Configuration](#step-41-docker-compose-configuration)
      - [Step 4.2: Build and Run the Bot with Docker](#step-42-build-and-run-the-bot-with-docker)
  - [Updating the Bot](#updating-the-bot)
  - [Managing the Bot with Docker](#managing-the-bot-with-docker)
      - [Restart the bot:](#restart-the-bot)
      - [Stop the bot:](#stop-the-bot)
      - [View logs:](#view-logs)
  - [Bot Usage](#bot-usage)
  - [Error Handling](#error-handling)
  - [What's Next?](#whats-next)
  - [Contact](#contact)

## Features
- Manage Hetzner servers directly via Telegram.
- Power servers on/off, reboot, and delete them.
- Support for Docker on multiple platforms (Linux/amd64, Linux/arm64).
- Robust error handling for both Hetzner API and bot operations.

## Requirements
- Python 3.11
- Hetzner API Token
- Telegram Bot Token
- Docker and Docker Compose

## Getting Started

### 1. Setting Up the Server

#### Step 1.1: Update the Server

Ensure your server is up to date by running:

```bash
sudo apt update && sudo apt upgrade -y
```

#### Step 1.2: Install Docker

If Docker isn't already installed, set it up with:

```bash
curl -fsSL https://get.docker.com | sh
```

### 2. Clone the Repository

Clone the ServerManagerBot repository and navigate to the project directory:

```bash
git clone https://github.com/erfjab/ServerManagerBot.git
cd ServerManagerBot
```

### 3. Configure the Bot

#### Step 3.1: Copy the Example Configuration

Copy the example configuration file to create a new configuration file:

```bash
cp data/.info.json.example data/.info.json
```

#### Step 3.2: Edit the Configuration

Open the `data/.info.json` file and insert your **Telegram Bot Token** and **Hetzner API keys**:

```bash
nano data/.info.json
```

Replace the placeholders with your information:

```json
{
  "TELEGRAM_BOT_TOKEN": "your-telegram-bot-token",
  "TELEGRAM_BOT_ADMINS": {
    "admin_chat_id": "hetzner_api_token"
  }
}
```

- **TELEGRAM_BOT_TOKEN**: Get this from [Telegram BotFather](https://t.me/botfather).
- **TELEGRAM_BOT_ADMINS**: Map your Telegram chat IDs to their Hetzner API tokens. Your `chat_id` is your Telegram user ID.

> [!TIP]  
> [Click here](https://docs.hetzner.com/cloud/api/getting-started/generating-api-token/) for instructions on generating a Hetzner API token.

### 4. Docker Setup

#### Step 4.1: Docker Compose Configuration

Ensure your `docker-compose.yml` is set up like this:

```yaml
services:
  ServerManagerBot:
    image: erfjab/ServerManagerBot:latest
    restart: always
    volumes:
      - ./data/:/code/data/
```

#### Step 4.2: Build and Run the Bot with Docker

1. **Pull the latest Docker image**:

    ```bash
    docker compose pull
    ```

2. **Start the bot**:

    ```bash
    docker compose up -d
    ```

3. **Verify the bot is running**:

    ```bash
    docker compose ps
    ```

This command lists the running containers.

## Updating the Bot

To update the bot to the latest version:

1. **Pull the latest Docker image**:

    ```bash
    docker compose pull
    ```

2. **Restart the bot**:

    ```bash
    docker compose up -d
    ```

## Managing the Bot with Docker

#### Restart the bot:

```bash
docker compose restart
```

#### Stop the bot:

```bash
docker compose down
```

#### View logs:

To check real-time logs of the bot:

```bash
docker compose logs -f
```

## Bot Usage

- Start a chat with the bot on Telegram.
- Use the `/start` command to view a list of your Hetzner servers.
- Execute actions such as powering on/off, rebooting, and resetting passwords.

## Error Handling

The bot includes comprehensive error handling for:
- Hetzner API issues.
- Connection problems.
- Invalid user inputs.

All errors are logged and can be monitored using Docker logs.

## What's Next?

- [x] Show Servers List
- [x] Display Full Server Info
- [x] Power On Servers
- [x] Power Off Servers
- [x] Perform Reset (Power Cycle)
- [x] Reset Root Password
- [x] Delete Servers
- [x] Rebuild (all images)
- [x] Reboot Servers
- [x] Provide Exclusive Access for Each Admin
- [ ] Create New Servers
- [ ] Set Server Limits for Admins
- [ ] Implement Dedicated Proxies for Access
- [ ] Change Server IP
- [ ] Manage Server IP Types (Add/Delete)

## Contact

- Telegram Channel: [@ErfJabs](https://t.me/ErfJabs)

Feel free to ⭐ the project to show your support!

[![Stargazers over time](https://starchart.cc/erfjab/ServerManagerBot.svg?variant=adaptive)](https://starchart.cc/erfjab/ServerManagerBot)