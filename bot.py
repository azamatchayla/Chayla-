import logging
from aiogram import Bot, Dispatcher, executor, types
from handlers.start import register_start_handlers
from handlers.catalog import register_catalog

API_TOKEN = "8093095032:AAEjxLVMzhRdKCpyGQ2SNyedppPPwSZQtaA"  # <- Sizning bot tokeningiz

# Log yozuvini sozlash
logging.basicConfig(level=logging.INFO)

# Bot va dispatcher obyektlari
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Handler funksiyalarini ro‘yxatdan o‘tkazish
register_start_handlers(dp)
register_catalog(dp)

# Botni ishga tushirish
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
