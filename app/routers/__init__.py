from aiogram import Router

from . import base
from .servers import setup_server_routers
from .users import setup_user_routers

__all__ = [
    "setup_routers",
    "setup_server_routers",
    "base",
]


def setup_routers() -> Router:
    router = Router()
    router.include_router(base.router)
    router.include_router(setup_server_routers())
    router.include_router(setup_user_routers())
    return router
