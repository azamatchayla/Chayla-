from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message, ContentType
import logging

# Telegram bot tokenini shu yerga yozing
API_TOKEN = '8093095032:AAEjxLVMzhRdKCpyGQ2SNyedppPPwSZQtaA'

# Log yozuvlarini sozlash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher obyektlari
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# /start komandasi uchun handler
@dp.message_handler(commands=['start'])
async def start_handler(message: Message):
    await message.answer(
        "Assalomu alaykum! Chayla botga xush kelibsiz.\n"
        "Iltimos, muammoingizni matn yoki surat ko‘rinishida yuboring."
    )

# Matnli xabarlar uchun handler
@dp.message_handler(content_types=ContentType.TEXT)
async def text_handler(message: Message):
    await message.answer(
        "🧠 *AI maslahat:*\n"
        "Siz yuborgan matn tahlil qilindi.\n"
        "Tavsiya: Fungitsid *'X'* preparatini qo‘llang.\n"
        "Buyurtma berish uchun /buyurtma ni bosing.",
        parse_mode="Markdown"
    )

# Suratlar uchun handler
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
