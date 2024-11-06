"""
Middleware for handling admin access in Telegram bot updates.
"""

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Update

from utils import logger, Storage, EnvSettings


# pylint: disable=too-few-public-methods
class CheckAdminAccess(BaseMiddleware):
    """
    Middleware to check if the user is an admin based on their user ID.
    This middleware processes incoming updates and allows only admins
    to proceed with the handler.
    """

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        user = None
        if event.message:
            user = event.message.from_user
            await Storage.add_log_message(user.id, event.message.message_id)
        elif event.callback_query:
            user = event.callback_query.from_user
        elif event.inline_query:
            user = event.inline_query.from_user
        elif event.chosen_inline_result:
            user = event.chosen_inline_result.from_user

        if not user:
            logger.warning("Received update without user information!")
            return None

        if user.id not in EnvSettings.TELEGRAM_ADMINS_ID:
            logger.warning("Blocked %s", user.username or user.first_name)
            return None

        return await handler(event, data)
