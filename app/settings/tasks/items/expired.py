from collections import defaultdict
from app.api import ClinetManager
from app.db import crud
from app.bot import bot
from app.settings.config import env


async def monitoring_expired():
    servers = await crud.get_servers()

    for server in servers:
        if not server.is_online or not server.expired_stats:
            continue

        categories = defaultdict(list)
        page, size = 1, server.size_value

        while True:
            users = await ClinetManager.get_users(server=server, page=page, size=size)
            if not users:
                break

            for user in users:
                categories["total"].append(user.username)
                if user.last_expired_hour and user.last_expired_hour < 24:
                    categories["today_expired"].append(user.username)
            page += 1

        bot_info = await bot.get_me()
        expired_list = (
            ",".join(
                f"<a href='https://t.me/{bot_info.username}?start=user_{server.id}_{username}'> <code>{username}</code> </a>"
                for username in categories["today_expired"]
            )
            or "<code>None</code>"
        )
        USERS_STATS = f"📊 <b>Users scheduled to expire today in {server.remark.title()} server:</b>\n⚰️ <b>List of users[<code>{len(categories['today_expired'])}</code>/<code>{len(categories['total'])}</code>]:</b> {expired_list}"

        for admin in env.TELEGRAM_ADMINS_ID:
            try:
                await bot.send_message(
                    chat_id=admin,
                    text=USERS_STATS,
                )
            except Exception:
                pass
