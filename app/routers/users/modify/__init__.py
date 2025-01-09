from aiogram import Router

from . import base, configs, confirm, owner

__all__ = ["setup_user_modify_routers", "base", "configs", "confirm", "owner"]


def setup_user_modify_routers() -> Router:
    router = Router()

    router.include_router(configs.router)
    router.include_router(confirm.router)
    router.include_router(owner.router)

    return router
