"""
Module docstring: This module contains functions for formatting user information
for display, including user status, data limit, subscription, etc.
"""

from datetime import datetime
from marzban import UserResponse
from utils import MessageTexts


def user_info(user: UserResponse) -> str:
    """
    Formats the user information for display.
    """
    return (MessageTexts.USER_INFO).format(
        status_emoji="🟣" if user.status == "on_hold" else "🟢",
        username=user.username,
        data_limit=round((user.data_limit / (1024**3)), 3),
        date_limit=(
            int(user.on_hold_expire_duration / (24 * 60 * 60))
            if user.status == "on_hold"
            else (user.expire - datetime.utcnow().timestamp()) // (24 * 60 * 60)
        ),
        subscription=user.subscription_url,
    )
