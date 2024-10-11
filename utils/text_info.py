from marzban import UserResponse
from utils.lang import MessageTexts
from datetime import datetime


def user_info(user: UserResponse) -> str:
    return (MessageTexts.UserInfo).format(
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
