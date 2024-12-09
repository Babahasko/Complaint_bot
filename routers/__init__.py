__all__ = ("router",)

from aiogram import Router
from .commands import router as commands_router
from .service import router as service_router

router = Router(name=__name__)

router.include_routers(
    commands_router,
    service_router,
)