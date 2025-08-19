# src/app.py
from __future__ import annotations

from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from loguru import logger

from core.config import settings
from bot.router import setup_routers  # Guruh/DM handlerlarini ulaymiz

app = FastAPI(title="Chayla Intake Bot")

# Aiogram obyektlari
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
setup_routers(dp)  # 🔗 routerlar ulandi


@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.on_event("startup")
async def on_startup():
    """
    Server ishga tushganda webhookni o‘rnatamiz.
    Render/hostingda WEBHOOK_URL ni Environment Variables’da berish shart.
    """
    if settings.WEBHOOK_URL:
        try:
            await bot.set_webhook(url=settings.WEBHOOK_URL, drop_pending_updates=True)
            logger.info(f"Webhook set: {settings.WEBHOOK_URL}")
        except Exception as e:
            logger.exception(f"Webhook set error: {e}")
    else:
        logger.warning("WEBHOOK_URL topilmadi — webhook o‘rnatilmadi (faqat /healthz ishlaydi).")


@app.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Telegram’dan kelgan yangilanishlarni Aiogram Dispatcher’ga uzatadi.
    """
    try:
        data = await request.json()
        update = Update.model_validate(data)
    except Exception as e:
        logger.exception("Webhook: update parse xatosi")
        raise HTTPException(status_code=400, detail=f"Bad request: {e}")

    try:
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.exception("Dispatcher xatolik (handlerlarda xato bo‘lishi mumkin).")

    # Telegram 200 kutadi — doim ok qaytaramiz
    return {"ok": True}
