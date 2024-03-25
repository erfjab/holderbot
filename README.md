![Example Image](holderbotcover.png)

<p align="center">
  <a href="./README.md">
	English
	</a>
	|
	<a href="./README_ru.md">
	Русский
	</a>
	|
	<a href="./README_fa.md">
	فارسی
	</a>

</p>

# What is Holderbot? #

Holder Bot is a quick and simple bot designed to address the issue of the lack of a timer start option after the initial connection in the "Marzban Panel" user interface. Utilizing the programming interfaces of Marzban Panel, Holder Bot provided users with the ability to easily utilize this feature on Telegram. However, after the 3.0 update, Holder Bot has enhanced its capabilities with the introduction of special features, reaching its peak in subsequent versions. Now, Holder Bot serves as a professional assistant for Marzban users. For more information, you can refer to the update section or join the Telegram channel.

> [!IMPORTANT]
> You can show your support by giving a star to this project on GitHub.
> We have created a Telegram channel for announcements, surveys, and interaction with users. You can join us via [@ErfjabHolderbot](https://t.me/erfjabholderbot).

# Why Holderbot?

- Ability to automatically configs upon reaching the limit of volume or time.
- Ability to manage panel admins (change password or sudo)
- Ability to add or remove admins for the panel
- Ability to determine the node consumption coefficient
- Ability to manage nodes (deactivate/activate/reconnect)
- Ability to monitor and receive notifications of node disconnections
- Ability to deactivate/activate monitoring
- Ability to change the monitoring timer for nodes
- Ability to create users in bulk/individually (on_hold)
- Ability to create users via templates
- Ability to create templates (volume, time, inbounds)
- Ability to get the last online time, sub-user update (individual)
- Ability to directly receive barcode and sub-link text or delete user
- Ability to receive the software used by the user
- Ability to receive a barcode for a desired sent link
- Ability to search and get similar users (like Google's Did you Mean)
- Ability to get a list of online/offline users 
- (from 1 minute to the last 60 days in table and PDF format)
- Ability to get a list of updated/not updated sub-users 
- (from 1 minute to the last 60 days in table and PDF format)
- New sleek and simple user interface.

> [!NOTE]
> We are constantly working on new updates. Do you have any ideas or suggestions? Please raise them as issues, and we will consider adding them in future updates.

# How to install Holderbot? #

To use the holderbot , you will need the following information:
1. **Name:** You can enter any name you prefer.
2. **Chat ID:** You need to obtain this from the [@chatIDrobot](https://t.me/chatIDrobot).
3. **Bot Token:** You need to obtain this from the [@botfather](https://t.me/BotFather).
4. **Panel Username:** Enter your panel sudo admin username.
5. **Panel Password:** Enter your panel sudo admin password.
6. **Panel Domain:** Enter your panel domain in this format (sub.domain.com:port).

> [!WARNING]
> Please note that HolderBot is currently only supported for installation and use on 
Ubuntu servers, and any responsibility for other setups is your own.

Please use the following command to install on your server:

```
cd && cd .. && rm -f holderbot.sh* || true && clear && wget https://raw.githubusercontent.com/erfjab/holderbot/main/holderbot.sh && chmod +x holderbot.sh && ./holderbot.sh
```

# How to use the bot? (video) # 

[![click me](https://github.com/erfjab/holderbot/blob/main/tumb.jpg)](https://www.youtube.com/watch?v=BqZvKV17uq0)

All explanations are complete and clear, but if you still notice any deficiencies or shortcomings in the explanations, please create an issue, and we will address it. Thank you for your cooperation.

> [!WARNING]
> These tutorials are exclusively for version 4. Previous versions are no longer supported.

## 🏛 Home Page

about the homepage, you'll find all the necessary commands listed, with detailed explanations provided further down the page. Here, besides entering commands, you can also send the username or link of your subscription. If the user exists, you'll receive their statistics, and if they don't , with Holder Bot's search feature to receive a list of similar users.

When user statistics are sent to you, you'll see three options: "Update," "Qrcode," and "Delete." To update the user's statistics, use the "Update" button. To receive the barcode for the user's subscription link, use the "Barcode" button. And to delete the user, use the "Delete" button. 

> [!NOTE]
> Don't worry, before carrying out the deletion operation, you will be asked for confirmation.

## 🚀 Create User

You have two options for creating a user: either through templates or manually. You can create ready-made templates by referring to the 'templates' section in this tutorial and creating your templates. When creating a user, if you click on one of your templates, the inbounds, volume, and time are pre-selected, and you will be asked for your username and the desired number. The bot automatically numbers the usernames and creates the users.

If you want to do this manually, you will be asked for inbounds, volume, and time, which is more suitable for specific cases. Templates speed up your work and allow you to create hundreds of users in a fraction of a second.

## 🎖 Notice

Welcome to the Messages section! This feature has been added with sponsorship the [Gray](https://t.me/GrayServer) collection.❤️ You can visit the Gray collection channel and bot for purchasing servers on an hourly and monthly basis, with a wide variety of locations and specifications, accompanied by clean IPs at the lowest prices. Before activating the Notice, you need to create an inbound Shadowsocks with the name "Holderbot" inside the panel:

```
{
  "tag": "Holderbot",
  "listen": "0.0.0.0",
  "port": 2222,
  "protocol": "shadowsocks",
  "settings": {
    "clients": [],
    "network": "tcp,udp"
  }
}
```
Then, inside the host settings of the inbound, we put our desired messages. After applying the changes, inside the Holderbot, we click on the "Change Status" option in the Notice section, and this feature becomes active. Holderbot checks users every 5 seconds and activates the messages for completed users, notifying you accordingly.

## 👤 Users

In the Users section, you receive general statistics of your panel. The number of users "all," "activated," "disabled," "on_hold," "limited," and "expired," along with the count of users who were online or offline in the last 24 hours, and whether their links have been updated or not, are provided.

Below, you'll find options where clicking on them will provide you with a list of user names in PDF format. If you click on the last two options, you'll be prompted for your desired timeframe, and based on that, you'll receive the statistics.

> [!TIP]
> If you have a specific timeframe in mind, you can enter it based on the pattern 'time min/hour/day'.

## 👨🏻‍💻 Admins

You can fully manage the panel admins in this section. You can add admins, remove admins, change admin passwords, and modify admin permissions. Just note that for removing sudo admins, it can only be done from the master server using the CLI command. APIs do not allow us access to this capability.

## 🎗 Nodes

You can also manage your servers here, reconnect, deactivate, activate, or set the consumption coefficient for your desired server. For monitoring and receiving server disconnection notifications, refer to the monitoring section on this page.

## 🗃 Templates

By creating templates, you can easily manage repetitive tasks, such as specifying volume, duration, and inbounds. In the templates section, you can create a new template or delete existing ones. To create a new template, simply click on "➕ Add new template." In the first step, enter the name without spaces, numbers, or icons. Then enter the volume (in gigabytes) and duration (in days), and finally select the inbounds. Each selected inbound marked with ➕ is included, while those marked with ➖ are not. After completing your selection, click "✅ finish" to save the template. To delete a template, simply click on it, and you'll be asked for confirmation. Once confirmed, it will be deleted.

> [!NOTE]
> You add/remove templates in this section, but you only use them in the "🚀 Create User" section.

## 🎛 Monitoring

Monitoring for your servers is enabled by default during the installation of HolderBot. You can enable/disable it from this section. You can also set the server check interval for monitoring and specify the waiting time for the next check when receiving a server disconnection notification.

## 🔍 Search

Sometimes you may not remember the username completely but want to input a few letters for the bot to find it easily and tell you. Is this what you mean? This capability is specifically designed for searches of this nature, where the bot can list the usernames similar to your input and send them to you.

> [!NOTE]
> This section is not for receiving user statistics. For that purpose, you can refer to the homepage tutorial.

## 💬 Help

A guide on solving problems, requesting assistance, reporting bugs, contacting the developer, and similar matters will be sent to you. Additionally, a file containing Holder Bot logs will be sent to you, which you can share with the developer if needed for debugging and problem-solving.

## 🖼 QR Code

You can receive its barcode by sending any link or text. This feature is not exclusive to v2ray links, and it can provide you with its barcode in code form for any received link. It's quick and simple!

> [!TIP]
> You can modify the barcode color in the "qr.py" file in the "Function" folder using line 8 (fill_color) with options like red, pink, blue, yellow.

<p align="center">
  <a target="_blank" href="https://t.me/ErfjabHolderbot">
    <img alt="Telegram Badge" src="https://img.shields.io/badge/holderbotchanel-Telegramlink?style=for-the-badge&logo=telegram&logoColor=white&color=blue&link=https%3A%2F%2Ft.me%2FErfjabHolderbot&link=https%3A%2F%2Ft.me%2FErfjabHolderbot">
  </a>
</p>

<p align="center">
	<picture>
	  <source
	    media="(prefers-color-scheme: dark)"
	    srcset="
	      https://api.star-history.com/svg?repos=erfjab/holderbot&type=Date&theme=dark
	    "
	  />
	  <source
	    media="(prefers-color-scheme: light)"
	    srcset="
	      https://api.star-history.com/svg?repos=erfjab/holderbot&type=Date
	    "
	  />
	  <img
	    alt="Star History Chart"
	    src="https://api.star-history.com/svg?repos=erfjab/holderbot&type=Date"
	  />
	</picture>
</p>
