"""
Module docstring: This module contains functions for formatting user information
for display, including user status, data limit, subscription, etc.
"""

from typing import Optional
from datetime import datetime, timezone
from marzban import UserResponse
from utils import MessageTexts


def user_info(user: UserResponse) -> str:
    """
    Formats user information with detailed time remaining display.
    """

    def format_traffic(bytes_val: Optional[int]) -> str:
        if not bytes_val and bytes_val != 0:
            return "♾️"
        return f"{round(bytes_val / (1024**3), 1)}"

    def format_time_remaining(timestamp: Optional[int]) -> str:
        if not timestamp:
            return "♾️"

        now = datetime.now(timezone.utc)
        expire_date = datetime.fromtimestamp(timestamp, tz=timezone.utc)

        if now > expire_date:
            return "Expired"

        diff = expire_date - now
        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60

        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    def format_ago(dt_str: Optional[str]) -> str:
        if not dt_str:
            return "➖"
        try:
            dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            diff = datetime.now(timezone.utc) - dt
            days = diff.days
            hours = diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60

            if days > 0:
                return f"{days}d ago"
            if hours > 0:
                return f"{hours}h ago"
            return f"{minutes}m ago"
        except ValueError:
            return "Invalid date"

    status_emojis = {"on_hold": "🟣", "active": "🟢"}
    template = (
        MessageTexts.ACCOUNT_INFO_ONHOLD
        if user.status == "on_hold"
        else MessageTexts.ACCOUNT_INFO_ACTIVE
    )

    return template.format(
        username=user.username or "Unknown",
        status=user.status or "unknown",
        status_emoji=status_emojis.get(user.status, "🔴"),
        data_used=format_traffic(user.used_traffic),
        data_limit=format_traffic(user.data_limit),
        date_used=format_traffic(user.used_traffic),
        date_limit=format_traffic(user.data_limit),
        date_left=format_time_remaining(user.expire),
        data_limit_reset_strategy=user.data_limit_reset_strategy or "None",
        created_at=format_ago(user.created_at),
        online_at=format_ago(user.online_at),
        sub_update_at=format_ago(user.sub_updated_at),
        subscription_url=user.subscription_url or "None",
        on_hold_expire_duration=round((user.on_hold_expire_duration or 0) / 86400, 1),
    )
