from aiogram import Router

from . import menu, create, data

__all__ = ["setup_template_routers", "menu", "create", "data"]


def setup_template_routers() -> Router:
    router = Router()

    router.include_router(menu.router)
    router.include_router(create.router)
    router.include_router(data.router)

    return router
