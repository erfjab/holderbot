"""
This module handles updating the Marzban panel token at regular intervals.
"""

import httpx

from marzban import MarzbanAPI
from utils import EnvSettings, logger
from db.crud import TokenManager
from models import TokenUpsert


async def token_update() -> bool:
    """Add or update Marzban panel token every X time."""
    if not EnvSettings.MARZBAN_USERNAME or not EnvSettings.MARZBAN_PASSWORD:
        logger.error("MARZBAN_USERNAME or MARZBAN_PASSWORD is not set.")
        return False

    api = MarzbanAPI(base_url=EnvSettings.MARZBAN_ADDRESS)

    try:
        get_token = await api.get_token(
            username=EnvSettings.MARZBAN_USERNAME, password=EnvSettings.MARZBAN_PASSWORD
        )

        if get_token and get_token.access_token:
            token_data = await TokenManager.upsert(
                TokenUpsert(token=get_token.access_token)
            )
            if token_data:
                logger.info("Token updated successfully.")
                return True

            logger.error("Failed to update token in database.")
            return False

        logger.error("Failed to retrieve token: No token received.")
        return False

    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        logger.error("An error occurred during the API request: %s", str(e))
        return False
