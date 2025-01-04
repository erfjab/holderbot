from aiogram import Router

from . import menu, data

__all__ = ["setup_user_routers", "menu", "data"]


def setup_user_routers() -> Router:
    router = Router()

    router.include_router(menu.router)
    router.include_router(data.router)

    return router
