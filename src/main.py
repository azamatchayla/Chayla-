# src/main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from loguru import logger

from core.config import settings
from bot.router import setup_routers  # Barcha handler routerlarini shu yerda ulaymiz


def _setup_logging():
    logger.remove()
    logger.add(lambda msg: print(msg, end=""))  # oddiy stdout
    logger.info("Logging initialized")


# /start komandasi uchun fallback (DM va guruhda ham ishlaydi)
async def _register_fallback(dp: Dispatcher):
    @dp.message(commands=["start"])
    async def cmd_start(message: Message):
        await message.reply(
            "👋 Salom! Men **Chayla**.\n"
            "Agrar savollar
