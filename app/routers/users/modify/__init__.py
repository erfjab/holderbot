from aiogram import Router

from . import base, configs, confirm, datalimit, owner, datelimit, note

__all__ = [
    "setup_user_modify_routers",
    "base",
    "configs",
    "confirm",
    "owner",
    "datalimit",
    "datelimit",
    "note",
]


def setup_user_modify_routers() -> Router:
    router = Router()

    router.include_router(configs.router)
    router.include_router(confirm.router)
    router.include_router(owner.router)
    router.include_router(datalimit.router)
    router.include_router(datelimit.router)
    router.include_router(note.router)

    return router
