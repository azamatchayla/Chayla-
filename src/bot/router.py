# src/bot/router.py
from aiogram import Dispatcher
from .handlers.group import router as group_router
from .handlers.private import router as private_router

def setup_routers(dp: Dispatcher) -> None:
    """
    Barcha routerlarni tartib bilan ulaydi.
    Avval DM (private), keyin group — shunda /start va DM oqimlari to'g'ri ishlaydi.
    """
    dp.include_routers(
        private_router,
        group_router,
    )
