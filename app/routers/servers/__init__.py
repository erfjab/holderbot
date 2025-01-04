from aiogram import Router

from . import create, data

__all__ = ["setup_server_routers", "creat", "data"]


def setup_server_routers() -> Router:
    router = Router()

    router.include_router(create.router)
    router.include_router(data.router)

    return router
