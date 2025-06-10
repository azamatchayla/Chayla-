from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 🟩 Asosiy menyu tugmalari
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("🤖 AI maslahat"),
    KeyboardButton("🌾 Ekinlar toifasi")
)
main_menu.add(KeyboardButton("📦 Buyurtmalar"))

# 🌾 Ekinlar toifalari
crop_categories = ReplyKeyboardMarkup(resize_keyboard=True)
crop_categories.add(
    KeyboardButton("🏡 Issiqxona"),
    KeyboardButton("🌳 Bog‘"),
    KeyboardButton("🌱 Ochiq dala")
)
crop_categories.add(
    KeyboardButton("🏠 Uy tomorqasi"),
    KeyboardButton("🥬 Sabzavotzor")
)
crop_categories.add(
    KeyboardButton("🌾 Baxmal yem-xashaklar"),
    KeyboardButton("🌺 Manzarali o‘simliklar")
)
crop_categories.add(KeyboardButton("⬅️ Orqaga"))

# 🍅 Issiqxona ichidagi ekinlar
greenhouse_crops = ReplyKeyboardMarkup(resize_keyboard=True)
greenhouse_crops.add(
    KeyboardButton("Pomidor"),
    KeyboardButton("Bodring"),
    KeyboardButton("Baqlajon")
)
greenhouse_crops.add(KeyboardButton("⬅️ Orqaga"))

# Pomidor uchun bo‘limlar
pomidor_sections = ReplyKeyboardMarkup(resize_keyboard=True)
pomidor_sections.add(
    KeyboardButton("🌿 Gerbitsidlar"),
    KeyboardButton("🪲 Insektitsidlar"),
    KeyboardButton("🍄 Fungitsidlar")
)
pomidor_sections.add(
    KeyboardButton("💊 O‘g‘itlar"),
    KeyboardButton("🔄 Boshqalar"),
    KeyboardButton("⬅️ Orqaga")
)
