"""check telegram users access to bot before any request"""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

from app.settings import EnvFile, logger


class CheckUserAccess(BaseMiddleware):
    """check user access to use bot"""

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        user = None
        if event.message:
            user = event.message.from_user
        elif event.callback_query:
            user = event.callback_query.from_user
        elif event.inline_query:
            user = event.inline_query.from_user
        elif event.chosen_inline_result:
            user = event.chosen_inline_result.from_user

        if not user:
            logger.warning("Received update without user information!")
            return None

        if not EnvFile.is_admin(user.id):
            logger.warning(
                f"Blocked {'@' + user.username or user.first_name} [{user.id}]"
            )
            return None

        return await handler(event, data)
