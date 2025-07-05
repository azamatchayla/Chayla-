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

# User photo cache
user_photos = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌱 Chayla AI ishga tushdi. Surat yuboring, so‘ng izoh yoki savol yozing.")

# Photo handler
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
        logger.error(f"Photo error: {e}")
        await update.message.reply_text("❗ Suratni qabul qila olmadim. Qayta urinib ko‘ring.")

# Text handler
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    try:
        if user_id in user_photos:
            # Rasm + matn birga yuboriladi
            img_base64 = user_photos[user_id]
            messages = [
                {"role": "system", "content": "Sen Chayla AI botisan. Surat va matnga qarab, fermerga qishloq xo'jaligi bo'yicha foydali maslahat ber."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text},
                        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_base64}"}
                    ]
                }
            ]
            del user_photos[user_id]
        else:
            # Faqat matn
            messages = [
                {"role": "system", "content": "Sen Chayla AI botisan. Qishloq xo'jaligi bo'yicha foydali maslahat ber."},
                {"role": "user", "content": text}
            ]

        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",
            messages=messages
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Text error: {e}")
        await update.message.reply_text("❗ Javob bera olmadim. Keyinroq urinib ko‘ring.")

# Run bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Chayla AI bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
