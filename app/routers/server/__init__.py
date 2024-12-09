from aiogram import Router
from . import create

__all__ = ["setup_server_routers", "home"]


def setup_server_routers() -> Router:
    """
    Sets up the routers for the bot application by including the necessary sub-routers.
    """
    router = Router()

    router.include_router(create.router)

    return router
