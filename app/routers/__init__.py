from aiogram import Router

from . import base
from .servers import setup_server_routers
from .users import setup_user_routers
from .actions import setup_action_routers

__all__ = [
    "setup_routers",
    "setup_server_routers",
    "setup_action_routers",
    "base",
]


def setup_routers() -> Router:
    router = Router()
    router.include_router(base.router)
    router.include_router(setup_server_routers())
    router.include_router(setup_user_routers())
    router.include_router(setup_action_routers())
    return router
