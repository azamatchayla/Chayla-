import os
import logging
import base64
from io import BytesIO
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Tokenlar
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Har bir userning rasmlarini vaqtincha saqlash
user_photos = {}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌱 Chayla AI bot ishga tushdi. Surat yuboring, so‘ng izoh yoki savolingizni yozing.")

# Rasmni qabul qilish
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        file_bytes = BytesIO()
        await file.download(out=file_bytes)
        file_bytes.seek(0)

        image = Image.open(file_bytes)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        user_id = update.message.from_user.id
        user_photos[user_id] = img_base64

        await update.message.reply_text("✅ Surat qabul qilindi. Endi izoh yoki savolingizni yozing.")
    except Exception as e:
    logger.error(f"Photo handling error: {e}")
    await update.message.reply_text("❗ Suratni qabul qila olmadim. Qayta urinib ko‘ring.")


