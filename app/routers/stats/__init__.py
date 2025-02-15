from aiogram import Router

from . import show

__all__ = ["setup_stats_routers", "show"]


def setup_stats_routers() -> Router:
    router = Router()

    router.include_router(show.router)

    return router
