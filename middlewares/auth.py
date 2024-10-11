from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Update
from utils.log import logger
from utils.config import TELEGRAM_ADMINS_ID
from utils.statedb import storage


class CheckAdminAccess(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        user = None
        if event.message:
            user = event.message.from_user
            await storage.add_log_message(user.id, event.message.message_id)
        elif event.callback_query:
            user = event.callback_query.from_user
        elif event.inline_query:
            user = event.inline_query.from_user
        elif event.chosen_inline_result:
            user = event.chosen_inline_result.from_user

        if not user:
            logger.warning("Received update without user information!")
            return None

        if user.id not in TELEGRAM_ADMINS_ID:
            logger.warning(f"Blocked {user.username or user.first_name}")
            return None

        return await handler(event, data)
