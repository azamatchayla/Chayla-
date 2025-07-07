import os
import logging
import base64
from io import BytesIO
from PIL import Image
import openai
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# Tokenlar
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI sozlash
openai.api_key = OPENAI_API_KEY

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Har bir userning rasmlari vaqtincha saqlanadi
user_photos = {}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ChaylaAI ishga tushdi! Surat yuboring, so‘ng izoh yoki savolingizni yozing.")

# Rasm qabul qilish
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        file_bytes = BytesIO()
        await file.download_to_memory(out=file_bytes)

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

# Matn qabul qilish va AI javob
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        user_message = update.message.text
        img_base64 = user_photos.get(user_id, None)

        messages = [
            {"role": "system", "content": "Sen Chayla AI agrobotisan. Foydalanuvchining savoliga rasm va matn asosida aniq va qisqa javob ber."},
            {"role": "user", "content": f"Matn: {user_message}\nRasm (base64): {img_base64 if img_base64 else 'Rasm yuborilmagan'}"}
        ]

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        reply_text = response.choices[0].message.content
        await update.message.reply_text(reply_text)

    except Exception as e:
        logger.error(f"AI handling error: {e}")
        await update.message.reply_text("❗ AI javobini olishda xatolik bo‘ldi. Keyinroq urinib ko‘ring.")

# Botni ishga tushirish
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
