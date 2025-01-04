from aiogram import Router

from . import menu, data

__all__ = ["setup_server_routers", "menu", "data"]


def setup_server_routers() -> Router:
    router = Router()

    router.include_router(menu.router)
    router.include_router(data.router)

    return router
