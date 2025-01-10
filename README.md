### HolderBot  

Telegram bot for managing panels with unique and advanced capabilities.

### Supported Panels  
- [x] **Marzneshin**  
- [ ] **Alireza**  
- [ ] **Hiddify**  
- [ ] **3x-ui**  


### Server and Docker Setup  

<details>
<summary>Show Server Commands</summary>

#### 1. Update the Server  
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Docker  
```bash
curl -fsSL https://get.docker.com | sh
```
</details>


### Run the Bot  

<details>
<summary>Show Run Commands</summary>


#### 1. Create Directory and Download Files  
```bash
mkdir -p /opt/erfjab/holderbot/data
curl -o /opt/erfjab/holderbot/docker-compose.yml https://raw.githubusercontent.com/erfjab/holderbot/master/docker-compose.yml
cd /opt/erfjab/holderbot
curl -o .env https://raw.githubusercontent.com/erfjab/holderbot/master/.env.example
nano .env
```

#### 2. Pull Docker Image  
```bash
docker compose pull
```

#### 3. Start the Bot  
```bash
docker compose up -d
```

After a few moments, start the bot.

</details>


### Update the Bot  

<details>
<summary>Show Update Commands</summary>

Make sure you're in the **HolderBot** directory:  
```bash
cd /opt/erfjab/holderbot
```

Then update the bot:  
```bash
docker compose pull && docker compose up -d
```

</details>


### Manage the Bot  

<details>
<summary>Show Manage Commands</summary>

Make sure you're in the **HolderBot** directory:  
```bash
cd /opt/erfjab/holderbot
```

- **Restart the Bot:**  
  ```bash
  docker compose restart
  ```

- **Stop the Bot:**  
  ```bash
  docker compose down
  ```

- **View Logs:**  
  ```bash
  docker compose logs -f
  ```

</details>


### Support  

Telegram Channel: [@ErfJabs](https://t.me/ErfJabs)  
Telegram Group: [@ErfJabGroup](https://t.me/erfjabgroup)  

⭐ **Star the project:**  
[![Stargazers](https://starchart.cc/erfjab/holderbot.svg?variant=adaptive)](https://starchart.cc/erfjab/holderbot)  