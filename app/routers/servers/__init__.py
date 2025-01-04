from aiogram import Router

from . import create, data, modify

__all__ = ["setup_server_routers", "creat", "data", "modify"]


def setup_server_routers() -> Router:
    router = Router()

    router.include_router(create.router)
    router.include_router(data.router)
    router.include_router(modify.router)

    return router
