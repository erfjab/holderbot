from aiogram import Router


def setup_routers() -> Router:

    from . import base, user, node

    router = Router()

    router.include_router(base.router)
    router.include_router(user.router)
    router.include_router(node.router)

    return router
