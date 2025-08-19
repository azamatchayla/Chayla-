# src/web/api.py
from __future__ import annotations

from fastapi import APIRouter, Request, HTTPException, FastAPI
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from loguru import logger

from core.config import settings

router = APIRouter()
_bot: Bot | None = None
_dp: Dispatcher | None = None


def attach(app: FastAPI, bot: Bot, dp: Dispatcher) -> None:
    """
    FastAPI ilovasiga routerni ulash va webhookni startda sozlash.
    app.py dan chaqiriladi:  attach(app, bot, dp)
    """
    global _bot, _dp
    _bot = bot
    _dp = dp

    app.include_router(router)

    @app.on_event("startup")
    async def _on_startup():
        if settings.WEBHOOK_URL:
            try:
                await _bot.set_webhook(url=settings.WEBHOOK_URL, drop_pending_updates=True)
                logger.info(f"[web] Webhook set: {settings.WEBHOOK_URL}")
            except Exception as e:
                logger.exception(f"[web] Webhook set error: {e}")
        else:
            logger.warning("[web] WEBHOOK_URL berilmagan, webhook o'rnatilmadi.")


@router.get("/healthz")
async def healthz():
    return {"ok": True}


@router.post("/webhook")
async def telegram_webhook(request: Request):
    if _bot is None or _dp is None:
        logger.error("[web] Bot/Dispatcher init qilinmagan")
        raise HTTPException(status_code=503, detail="Bot not initialized")

    try:
        data = await request.json()
        update = Update.model_validate(data)
    except Exception as e:
        logger.exception("[web] Update parse xatosi")
        raise HTTPException(status_code=400, detail=f"Bad request: {e}")

    try:
        await _dp.feed_update(_bot, update)
    except Exception as e:
        logger.exception("[web] Dispatcher xatolik")
        # Baribir 200 qaytaramiz — Telegram qayta yuborib ketmasin
    return {"ok": True}
