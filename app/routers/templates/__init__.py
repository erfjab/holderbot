from aiogram import Router

from . import menu

__all__ = ["setup_template_routers", "menu"]


def setup_template_routers() -> Router:
    router = Router()

    router.include_router(menu.router)

    return router
