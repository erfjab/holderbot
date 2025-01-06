from aiogram import Router, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from app.api import ClinetManager
from app.db import crud
from app.settings.language import MessageTexts

router = Router(name="inline")


@router.inline_query()
async def get(query: types.InlineQuery):
    texts = query.query.strip().split()
    results = []

    if len(texts) == 0:
        servers = await crud.get_servers()
        results = [
            InlineQueryResultArticle(
                id=str(server.id),
                title=f"{server.id} | {server.remark}",
                description=f"server type: {server.types}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Server ID: {server.id}\nRemark: {server.remark}",
                ),
                thumbnail_url="https://github.com/user-attachments/assets/02947eb3-421c-424c-8f64-83686168c8f5",
            )
            for server in servers
        ]
        return await query.answer(
            results=results,
            cache_time=10,
        )

    if not texts[0].isdigit():
        return await query.answer(
            results=[],
            switch_pm_text="Please enter a valid server ID (integer)",
            switch_pm_parameter="invalid_server_id",
            cache_time=10,
        )

    server_id = int(texts[0])
    server = await crud.get_server(server_id)
    if not server:
        return await query.answer(
            results=[],
            switch_pm_text="Server not found. Enter a valid server ID.",
            switch_pm_parameter="server_not_found",
            cache_time=10,
        )

    search = " ".join(texts[1:]) if len(texts) > 1 else None

    users = await ClinetManager.get_users(server=server, page=1, size=50, search=search)

    if not users:
        return await query.answer(
            results=[],
            switch_pm_text="No users found for the given query.",
            switch_pm_parameter="no_users_found",
            cache_time=10,
        )

    for user in users:
        user_info = MessageTexts.USER_INFO.format(**user.format_data)

        result = InlineQueryResultArticle(
            id=user.username,
            title=f"{user.emoji} {user.remark} ({user.owner_username})",
            description="data: {data_limit} | date: {expire_strategy}".format(
                **user.format_data
            ),
            input_message_content=InputTextMessageContent(
                message_text=user_info, parse_mode="HTML"
            ),
            thumbnail_url="https://github.com/user-attachments/assets/02947eb3-421c-424c-8f64-83686168c8f5",
        )
        results.append(result)

    await query.answer(results=results, cache_time=10)
