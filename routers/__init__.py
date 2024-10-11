from aiogram import Router


def setup_routers() -> Router:

    from . import base, user

    router = Router()

    router.include_router(base.router)
    router.include_router(user.router)

    return router
