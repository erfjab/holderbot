from aiogram import Router

from . import menu, data, create, modify

__all__ = ["setup_user_routers", "menu", "data", "create", "modify"]


def setup_user_routers() -> Router:
    router = Router()

    router.include_router(menu.router)
    router.include_router(data.router)
    router.include_router(create.router)
    router.include_router(modify.router)

    return router
