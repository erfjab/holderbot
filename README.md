# HolderBot  

A powerful Telegram bot for managing multiple VPN panels with advanced features and ease of use.

![holderbotcover](https://github.com/user-attachments/assets/db3b5da5-3e22-4436-9502-ed478415f908)

---

## **Supported Panels**  
- [x] **Marzneshin**  
- [x] **Marzban**  
- [ ] **Alireza**  
- [ ] **Hiddify**  
- [ ] **3x-ui**  

---

## **Features**  

### **Multi-Server & Multi-Panel Support**  
- Manage multiple servers and panels from a single bot.

### **Bulk User Creation**  
- Create users in bulk with custom admin selection.  
- Add custom suffixes to usernames.  
- Send QR codes and user data after creation (customizable).  
- Select custom data limits, expiration dates, and configurations.  
- Create users using predefined templates.

### **User Management**  
- **User Menu:**  
  - Filter users by status: active, expired, or limited.  
  - Display icons for user status.  
- **User Search:**  
  - Search users with `/user serverid username`.  
  - Show up to 10 users matching the search criteria.  
- **User Modifications:**  
  - Add notes.  
  - Set data and date limits.  
  - Activate or disable users.  
  - Charge users using templates (optional reset of data usage).  
  - Reset usage.  
  - Revoke subscriptions.  
  - Send QR codes with user data (customizable).  
  - Set or change the owner.  
  - Modify configurations.  
  - Remove users.

### **Admin Management**  
- Activate or deactivate admin users.  
- Delete expired, limited, or admin users.  
- Transfer users from one admin to another.  
- Add or remove configurations for all users.

### **Node Monitoring**  
- Monitor nodes for issues.  
- Automatically restart nodes if needed.

---

## **Setup**  

### **Server and Docker Setup**  

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

---

### **Install & Run the Bot**  

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

After a few moments, the bot will start running.

</details>

---

### **Update the Bot**  

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

---

### **Manage the Bot**  

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

---

### **Switch to GA Mode (preview mode)**  

<details>
<summary>Show GA Commands</summary>

Make sure you're in the **HolderBot** directory:  
```bash
cd /opt/erfjab/holderbot
```

- **Open the Docker Compose File:**  
  ```bash
  nano docker-compose.yml
  ```

- **Change the Image Tag:**  
  
  **From:**  
  ```yaml
  erfjab/holderbot:latest
  ```
  **To:**  
  ```yaml
  erfjab/holderbot:ga
  ```

- **Pull the Docker Image:**  
  ```bash
  docker compose pull
  ```

- **Start the Bot:**  
  ```bash
  docker compose up -d
  ```
</details>

---

## **Support**  

- **Telegram Channel:** [@ErfJabs](https://t.me/ErfJabs)  
- **Telegram Group:** [@ErfJabGroup](https://t.me/erfjabgroup)  

⭐ **Star the Project:**  
[![Stargazers](https://starchart.cc/erfjab/holderbot.svg?variant=adaptive)](https://starchart.cc/erfjab/holderbot)  
