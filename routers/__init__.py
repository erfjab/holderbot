"""
This module sets up the routers for the bot application.
It includes base, user, node, and users routers.
"""

from aiogram import Router
from . import base, user, node, users

__all__ = ["setup_routers", "base", "user", "node", "users"]


def setup_routers() -> Router:
    """
    Sets up the routers for the bot application by including the necessary sub-routers.
    """
    router = Router()

    router.include_router(base.router)
    router.include_router(user.router)
    router.include_router(node.router)
    router.include_router(users.router)

    return router
