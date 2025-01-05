### Server Setup

#### 1. Update the Server  
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Docker  
```bash
curl -fsSL https://get.docker.com | sh
```

---

### Download and Configure

#### 1. Create Directory and Download Files  
```bash
mkdir -p /opt/erfjab/holderbot/data
curl -o /opt/erfjab/holderbot/docker-compose.yml https://raw.githubusercontent.com/erfjab/holderbot/master/docker-compose.yml
cd /opt/erfjab/holderbot
curl -o .env https://raw.githubusercontent.com/erfjab/holderbot/master/.env.example
nano .env
```

---

### Run the Bot

#### 1. Pull Docker Image  
```bash
docker compose pull
```

#### 2. Start the Bot  
```bash
docker compose up -d
```

#### 3. Verify Bot Status  
```bash
docker compose ps
```

---

### Update the Bot  
```bash
docker compose pull && docker compose up -d
```

---

### Manage the Bot  

- Restart:  
  ```bash
  docker compose restart
  ```

- Stop:  
  ```bash
  docker compose down
  ```

- Logs:  
  ```bash
  docker compose logs -f
  ```

---

### Support  
Telegram: [@ErfJabs](https://t.me/ErfJabs)  

⭐ Star the project:  
[![Stargazers](https://starchart.cc/erfjab/holderbot.svg?variant=adaptive)](https://starchart.cc/erfjab/holderbot)  