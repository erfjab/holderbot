from utils.config import MARZBAN_PASSWORD, MARZBAN_USERNAME, MARZBAN_ADDRESS
from db.crud import TokenManager
from utils.log import logger
from models import TokenUpsert
from marzban import MarzbanAPI


async def token_update() -> bool:
    """Add or update Marzban panel token every X time."""
    if not MARZBAN_USERNAME or not MARZBAN_PASSWORD:
        logger.error("MARZBAN_USERNAME or MARZBAN_PASSWORD is not set.")
        return False

    api = MarzbanAPI(base_url=MARZBAN_ADDRESS)

    try:
        get_token = await api.get_token(
            username=MARZBAN_USERNAME, password=MARZBAN_PASSWORD
        )

        if get_token and get_token.access_token:
            token_data = await TokenManager.upsert(
                TokenUpsert(token=get_token.access_token)
            )
            if token_data:
                logger.info("Token updated successfully.")
                return True
            else:
                logger.error("Failed to update token in database.")
                return False

        logger.error("Failed to retrieve token: No token received.")
        return False

    except Exception as e:
        logger.error(f"An unexpected TOKEN_UPDATER error occurred: {str(e)}")
        return False
