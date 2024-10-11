import json

from marzban import MarzbanAPI, ProxyInbound, UserResponse, UserCreate
from datetime import datetime, timedelta
from utils.config import MARZBAN_ADDRESS
from db import TokenManager
from utils.log import logger

marzban_panel = MarzbanAPI(MARZBAN_ADDRESS)


async def inbounds() -> dict[str, list[ProxyInbound]]:
    try:
        get_token = await TokenManager.get()
        inbounds = await marzban_panel.get_inbounds(get_token.token)
        return inbounds or False
    except Exception as e:
        logger.error(f"Error getting token: {e}")
        return False


async def create_user(
    username: str,
    status: str,
    proxies: dict,
    inbounds: dict,
    data_limit: int,
    date_limit: int,
) -> UserResponse:
    try:
        get_token = await TokenManager.get()

        new_user = UserCreate(
            username=username,
            status=status,
            proxies=proxies,
            inbounds=inbounds,
            data_limit=(data_limit * (1024**3)),
            data_limit_reset_strategy="no_reset",
        )

        if status == "active":
            new_user.expire = int(
                (datetime.utcnow() + timedelta(days=date_limit)).timestamp()
            )

        elif status == "on_hold":
            new_user.on_hold_expire_duration = int(date_limit) * 86400
            new_user.on_hold_timeout = (datetime.utcnow() + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')

        user = await marzban_panel.add_user(new_user, get_token.token)
        return user or None
    except Exception as e:
        logger.error(f"Error create user: {e}")
        return False
