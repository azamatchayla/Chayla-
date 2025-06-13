import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ContentType
from aiogram.utils import executor

# Token environment variable (Render uses this)
API_TOKEN = os.getenv("BOT_TOKEN")

# Logging settings
logging.basicConfig(level=logging.INFO)

# Bot and Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# /start command
@dp.message_handler(commands=['start'])
async def start_handler(message: Message):
    await message.answer(
        "Assalomu alaykum! Chayla botga xush kelibsiz.\n"
        "Iltimos, muammoingizni matn yoki surat ko‘rinishida yuboring."
    )

# Text messages
@dp.message_handler(content_types=ContentType.TEXT)
async def text_handler(message: Message):
    await message.answer(
        "🧠 *AI maslahat:*\n"
        "Siz yuborgan matn tahlil qilindi.\n"
        "Tavsiya: Fungitsid *'X'* preparatini qo‘llang.\n"
        "Buyurtma berish uchun /buyurtma ni bosing.",
        parse_mode="Markdown"
    )

# Photo messages
@dp.message_handler(content_types=ContentType.PHOTO)
async def photo_handler(message: Message):
    await message.answer(
        "🧠 *AI maslahat:*\n"
        "Surat tahlil qilindi.\n"
        "Tavsiya: Insektitsid *'Y'* vositasidan foydalaning.\n"
        "Buyurtma berish uchun /buyurtma ni bosing.",
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)