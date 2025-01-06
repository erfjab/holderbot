from aiogram import Router

from . import menu
from .items import configs, users

__all__ = ["setup_action_routers", "menu", "configs", "users"]


def setup_action_routers() -> Router:
    router = Router()

    router.include_router(menu.router)
    router.include_router(configs.router)
    router.include_router(users.router)

    return router
