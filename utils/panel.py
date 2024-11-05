"""
This module provides functions to interact with the Marzban API,
including user management, retrieving inbounds, and managing admins.
"""

from datetime import datetime, timedelta
import httpx
from marzban import (
    MarzbanAPI,
    ProxyInbound,
    UserResponse,
    UserCreate,
    Admin,
    UserModify,
)
from db import TokenManager
from utils.config import MARZBAN_ADDRESS
from utils.log import logger

marzban_panel = MarzbanAPI(MARZBAN_ADDRESS, timeout=30.0, verify=False)


async def get_inbounds() -> dict[str, list[ProxyInbound]]:
    """
    Retrieve a list of inbounds from the Marzban panel.
    """
    try:
        get_token = await TokenManager.get()
        return await marzban_panel.get_inbounds(get_token.token) or False
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logger.error("Error getting panel inbounds: %s", e)
        return False


# pylint: disable=R0913, R0917
async def create_user(
    username: str,
    status: str,
    proxies: dict,
    inbounds: dict,
    data_limit: int,
    date_limit: int,
) -> UserResponse:
    """
    Create a new user in the Marzban panel.
    """
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
            new_user.on_hold_timeout = (
                datetime.utcnow() + timedelta(days=365)
            ).strftime("%Y-%m-%d %H:%M:%S")

        return await marzban_panel.add_user(new_user, get_token.token) or None
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logger.error("Error creating user: %s", e)
        return False


async def admins() -> list[Admin]:
    """
    Retrieve a list of admins from the Marzban panel.
    """
    try:
        get_token = await TokenManager.get()
        return await marzban_panel.get_admins(get_token.token) or False
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logger.error("Error getting admins list: %s", e)
        return False


async def set_owner(admin: str, user: str) -> bool:
    """
    Set an admin as the owner of a user.
    """
    try:
        get_token = await TokenManager.get()
        return (
            await marzban_panel.set_owner(
                username=user, admin_username=admin, token=get_token.token
            )
            is not None
        )
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logger.error("Error setting owner: %s", e)
        return False


async def user_modify(username: str, data: UserModify) -> bool:
    """
    Modify an existing user's details.
    """
    try:
        get_token = await TokenManager.get()
        return (
            await marzban_panel.modify_user(
                username=username, user=data, token=get_token.token
            )
            is not None
        )
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logger.error("Error modifying user: %s", e)
        return False


async def get_users(offset: int = 0, limit: int = 50) -> list[UserResponse]:
    """
    Retrieve a list of users from the Marzban panel.
    """
    try:
        get_token = await TokenManager.get()
        users_response = await marzban_panel.get_users(
            token=get_token.token, offset=offset, limit=limit
        )
        return users_response.users if users_response else False
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logger.error("Error getting all users: %s", e)
        return False
