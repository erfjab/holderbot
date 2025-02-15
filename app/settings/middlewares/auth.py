"""check telegram users access to bot before any request"""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

from app.settings.log import logger
from app.settings.config import env
from app.settings.track import tracker
from app.bot import bot


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
            await tracker.add(event.message)
        elif event.callback_query:
            user = event.callback_query.from_user
        elif event.inline_query:
            user = event.inline_query.from_user
        elif event.chosen_inline_result:
            user = event.chosen_inline_result.from_user

        if not user:
            logger.warning("Received update without user information!")
            return None

        if not env.is_admin(user.id):
            for admin in env.TELEGRAM_ADMINS_ID:
                try:
                    await bot.send_message(
                        chat_id=admin,
                        text=(
                            "<b>Oops, we have a spy!</b>\n"
                            f"🥷🏻 <b>Full Name:</b> <code>{user.full_name}</code>\n"
                            f"📌 <b>Username:</b> <code>{user.username or '➖'}</code>\n"
                            f"🆔 <b>User ID:</b> <code>{user.id}</code>\n"
                            f"🔗 <b>Private Chat Link:</b> <a href='tg://openmessage?user_id={user.id}'>Click here to open chat</a>"
                        ),
                    )
                except Exception:
                    pass

            logger.warning(
                f"Blocked {'@' + user.username or user.first_name} [{user.id}]"
            )
            return None

        return await handler(event, data)
