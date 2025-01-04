"""
Inline query handler for the bot.
Provides user search functionality through inline mode.
"""

from aiogram import Router, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from marzban import UsersResponse

from utils import panel, text_info, EnvSettings, BotKeyboards
from db.crud import TokenManager

router = Router()


@router.inline_query()
async def get(query: types.InlineQuery):
    """
    Handle inline queries to search and display user information.
    """
    text = query.query.strip()
    results = []

    emarz = panel.APIClient(EnvSettings.MARZBAN_ADDRESS)
    token = await TokenManager.get()
    users: UsersResponse = await emarz.get_users(
        search=text, limit=5, token=token.token
    )

    for user in users.users:
        user_info = text_info.user_info(user)

        result = InlineQueryResultArticle(
            id=user.username,
            title=f"{user.username}",
            description=f"Status: {user.status}",
            input_message_content=InputTextMessageContent(
                message_text=user_info, parse_mode="HTML"
            ),
            reply_markup=BotKeyboards.user(user),
        )

        results.append(result)

    await query.answer(results=results, cache_time=10)
