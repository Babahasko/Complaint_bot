__all__ = ("router",)

from aiogram import Router

from .handler_theme_commands import router as handler_theme_router
# from .handler_surveillance_commands import router as handler_object_router

router = Router(name=__name__)

router.include_routers(
    handler_theme_router,
    # handler_object_router,
)