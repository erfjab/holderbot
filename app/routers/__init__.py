from aiogram import Router
from . import home
from .server import setup_server_routers

__all__ = ["setup_routers", "home"]


def setup_routers() -> Router:
    """
    Sets up the routers for the bot application by including the necessary sub-routers.
    """
    router = Router()

    router.include_router(home.router)
    router.include_router(setup_server_routers())

    return router
