from aiogram import Router
from . import home

__all__ = ["setup_routers", "home"]


def setup_routers() -> Router:
    """
    Sets up the routers for the bot application by including the necessary sub-routers.
    """
    router = Router()

    router.include_router(home.router)

    return router
