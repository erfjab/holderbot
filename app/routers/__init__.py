from aiogram import Router

from . import base, inline
from .servers import setup_server_routers
from .users import setup_user_routers
from .actions import setup_action_routers
from .templates import setup_template_routers
from .stats import setup_stats_routers

__all__ = [
    "setup_routers",
    "setup_server_routers",
    "setup_action_routers",
    "setup_template_routers",
    "setup_stats_routers",
    "base",
    "inline",
]


def setup_routers() -> Router:
    router = Router()
    router.include_router(base.router)
    router.include_router(inline.router)
    router.include_router(setup_server_routers())
    router.include_router(setup_user_routers())
    router.include_router(setup_action_routers())
    router.include_router(setup_template_routers())
    router.include_router(setup_stats_routers())

    return router
