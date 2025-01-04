from aiogram import Router

from . import base

__all__ = [
    "setup_routers",
    "base",
]


def setup_routers() -> Router:
    router = Router()
    router.include_router(base.router)
    return router
