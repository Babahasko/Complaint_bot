__all__ = ("router",)

from aiogram import Router

from .handler_theme_commands import router as handler_theme_router

router = Router(name=__name__)

router.include_routers(
    handler_theme_router,
)