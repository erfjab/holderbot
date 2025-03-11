from aiogram import Router, F
from aiogram.types import CallbackQuery
from collections import defaultdict
from app.keys import BotKeys, PageCB, Pages, Actions
from app.db import crud
from app.settings.language import MessageTexts
from app.settings.track import tracker
from app.api import ClinetManager

router = Router(name="stats_data")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.STATS)) & (F.action.is_(Actions.LIST)))
)
async def show_stats(callback: CallbackQuery, callback_data: PageCB):
    server = await crud.get_server(callback_data.panel)
    if not server:
        track = await callback.message.edit_text(
            text=MessageTexts.NOT_FOUND, reply_markup=BotKeys.cancel()
        )
        return await tracker.add(track)

    await callback.message.edit_text(text="⏳")

    categories = defaultdict(list)
    page, size = 1, server.size_value

    while True:
        users = await ClinetManager.get_users(server=server, page=page, size=size)
        if not users:
            break

        for user in users:
            categories["total"].append(user.username)
            categories["enable" if user.is_enable else "disable"].append(user.username)
            if user.is_limited:
                categories["limited"].append(user.username)
            if user.is_expired:
                categories["expired"].append(user.username)
            if user.data_percent <= 1:
                categories["data_1"].append(user.username)
            if user.data_percent <= 10:
                categories["data_10"].append(user.username)
            if user.last_online_hour:
                if user.last_online_hour < 24:
                    categories["online_day"].append(user.username)
                if user.last_online_hour < (24 * 7):
                    categories["online_week"].append(user.username)
                if user.last_online_hour < (24 * 31):
                    categories["online_month"].append(user.username)
            if user.last_sub_update_hour:
                if user.last_sub_update_hour < 24:
                    categories["update_day"].append(user.username)
                if user.last_sub_update_hour < (24 * 7):
                    categories["update_week"].append(user.username)
                if user.last_sub_update_hour < (24 * 31):
                    categories["update_month"].append(user.username)
            if user.last_expired_hour and user.last_expired_hour <= 24:
                categories["today_expired"].append(user.username)
        page += 1

    USERS_STATS = (
        "📊 <b>Total:</b> <code>{total}</code>\n"
        "✅ <b>Enable:</b> <code>{enable}</code>\n"
        "🚫 <b>Disable:</b> <code>{disable}</code>\n"
        "⏳ <b>Expired:</b> <code>{expired}</code>\n"
        "⚠️ <b>Limited:</b> <code>{limited}</code>\n"
        "📉 <b>Remaining 1% Data Usage:</b> <code>{data_1}</code>\n"
        "📊 <b>Remaining 10% Data Usage:</b> <code>{data_10}</code>\n"
        "🕐 <b>Last Day Sub-Updated/Online:</b> <code>{update_day}</code>/<code>{online_day}</code>\n"
        "📆 <b>Last Week Sub-Updated/Online:</b> <code>{update_week}</code>/<code>{online_week}</code>\n"
        "📅 <b>Last Month Sub-Updated/Online:</b> <code>{update_month}</code>/<code>{online_month}</code>\n"
        "⚰️ <b>Expired in 24 Hours:</b> {today_expired}"
    )
    bot = await callback.bot.get_me()
    expired_list = (
        ",".join(
            f"<a href='https://t.me/{bot.username}?start=user_{server.id}_{username}'> <code>{username}</code> </a>"
            for username in categories["today_expired"]
        )
        or "<code>None</code>"
    )

    stats_text = USERS_STATS.format(
        total=len(categories["total"]),
        enable=len(categories["enable"]),
        disable=len(categories["disable"]),
        expired=len(categories["expired"]),
        limited=len(categories["limited"]),
        data_1=len(categories["data_1"]),
        data_10=len(categories["data_10"]),
        online_day=len(categories["online_day"]),
        online_week=len(categories["online_week"]),
        online_month=len(categories["online_month"]),
        update_day=len(categories["update_day"]),
        update_week=len(categories["update_week"]),
        update_month=len(categories["update_month"]),
        today_expired=expired_list,
    )

    track = await callback.message.edit_text(
        text=stats_text, reply_markup=BotKeys.cancel(server_back=server.id)
    )
    await tracker.add(track)
