from aiogram import Router

from . import menu, create, data
from .modify import base, confirm, datalimit, datelimit, remark

__all__ = [
    "setup_template_routers",
    "menu",
    "create",
    "data",
    "base",
    "confirm",
    "datalimit",
    "datelimit",
    "remark",
]


def setup_template_routers() -> Router:
    router = Router()

    router.include_router(menu.router)
    router.include_router(create.router)
    router.include_router(data.router)
    router.include_router(confirm.router)
    router.include_router(datelimit.router)
    router.include_router(datalimit.router)
    router.include_router(remark.router)

    return router
