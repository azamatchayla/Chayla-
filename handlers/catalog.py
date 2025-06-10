from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import Dispatcher

from keyboards.reply import crop_categories, greenhouse_crops, pomidor_sections, main_menu

async def crop_category_handler(message: types.Message):
    await message.answer("Ekinlar toifasini tanlang:", reply_markup=crop_categories)

async def greenhouse_handler(message: types.Message):
    await message.answer("Issiqxona ekinlarini tanlang:", reply_markup=greenhouse_crops)

async def pomidor_handler(message: types.Message):
    await message.answer("Pomidor uchun kerakli bo‘limni tanlang:", reply_markup=pomidor_sections)

async def back_to_main(message: types.Message):
    await message.answer("Asosiy menyuga qaytdingiz:", reply_markup=main_menu)

def register_catalog(dp: Dispatcher):
    dp.register_message_handler(crop_category_handler, lambda m: m.text == "🌾 Ekinlar toifasi")
    dp.register_message_handler(greenhouse_handler, lambda m: m.text == "🌿 Issiqxona")
    dp.register_message_handler(pomidor_handler, lambda m: m.text == "Pomidor")
    dp.register_message_handler(back_to_main, lambda m: m.text == "🔙 Orqaga")