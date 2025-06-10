from aiogram import types
from aiogram.dispatcher import Dispatcher

from keyboards.reply import main_menu

async def start_handler(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Chayla botga xush kelibsiz.",
        reply_markup=main_menu
    )

def register_start(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Asosiy menyu tugmalari
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("🤖 AI maslahat"),
    KeyboardButton("🌾 Ekinlar toifasi"),
    KeyboardButton("🛒 Buyurtmalar")
)

# Ekin toifalari (misol uchun)
crop_categories = ReplyKeyboardMarkup(resize_keyboard=True)
crop_categories.add(
    KeyboardButton("🏡 Uy tomorqasi"),
    KeyboardButton("🌿 Issiqxona"),
    KeyboardButton("🏞 Ochiq dala"),
    KeyboardButton("🌳 Bog‘"),
    KeyboardButton("🔙 Orqaga")
)

# Masalan, "Issiqxona" tanlanganda chiqadigan ekinlar
greenhouse_crops = ReplyKeyboardMarkup(resize_keyboard=True)
greenhouse_crops.add(
    KeyboardButton("Pomidor"),
    KeyboardButton("Bodring"),
    KeyboardButton("Baqlajon"),
    KeyboardButton("🔙 Orqaga")
)

# Masalan, Pomidor tanlanganda chiqadigan bo‘limlar
pomidor_sections = ReplyKeyboardMarkup(resize_keyboard=True)
pomidor_sections.add(
    KeyboardButton("🧪 Gerbitsidlar"),
    KeyboardButton("🐛 Insektitsidlar"),
    KeyboardButton("🍄 Fungitsidlar"),
    KeyboardButton("🌱 O‘g‘itlar"),
    KeyboardButton("🔙 Orqaga")
)

