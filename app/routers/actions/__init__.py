from aiogram import Router

from . import menu

__all__ = ["setup_action_routers", "menu"]


def setup_action_routers() -> Router:
    router = Router()

    router.include_router(menu.router)

    return router
