from aiogram import Router

from . import menu, data, create, search
from .modify import setup_user_modify_routers

__all__ = ["setup_user_routers", "menu", "data", "create", "search"]


def setup_user_routers() -> Router:
    router = Router()

    router.include_router(menu.router)
    router.include_router(data.router)
    router.include_router(create.router)
    router.include_router(search.router)
    router.include_router(setup_user_modify_routers())

    return router
