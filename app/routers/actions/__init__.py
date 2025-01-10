from aiogram import Router

from . import menu
from .items import configs, users, admin

__all__ = ["setup_action_routers", "menu", "configs", "users", "admin"]


def setup_action_routers() -> Router:
    router = Router()

    router.include_router(menu.router)
    router.include_router(configs.router)
    router.include_router(users.router)
    router.include_router(admin.router)

    return router
