# src/bot/handlers/private.py
from aiogram import Router, F
from aiogram.types import Message
from core.constants import START_TEXT, DRAFT_RESPONSE_FOOTER
from loguru import logger

router = Router()

# /start komandasi (DM uchun)
@router.message(F.text == "/start")
async def private_start(message: Message):
    await message.answer(START_TEXT)

# Foydalanuvchi DM’da matn yuborsa
@router.message(F.text & ~F.photo)
async def private_text(message: Message):
    logger.info(f"[PRIVATE] Matn: {message.from_user.id}")
    await message.answer(
        "Rahmat! Sizning yozganlaringiz qabul qilindi.\n"
        "Agar rasm ham yuborsangiz, xulosamiz aniqroq bo‘ladi."
    )

# Foydalanuvchi DM’da rasm yuborsa
@router.message(F.photo & ~F.text)
async def private_photo(message: Message):
    logger.info(f"[PRIVATE] Rasm: {message.from_user.id}")
    await message.answer(
        "Rahmat! Endi iltimos, qisqacha ma’lumot yozib yuboring:\n"
        "- Ekin nomi\n"
        "- Alomatlar (qachondan beri, qaysi qism)\n"
        "- Oxirgi ishlov (dori/doza/sana)\n"
        "- Hudud (viloyat/tuman)"
    )

# DM’da matn + rasm bo‘lsa
@router.message(F.photo & F.caption)
async def private_photo_with_caption(message: Message):
    logger.info(f"[PRIVATE] Matn+rasm: {message.from_user.id}")

    assessment = "Peronosporoz ehtimoli"
    solutions = "Flutriafol 25% EC (0.5 l/ga)\nMetomil 90% SP (0.6–0.8 kg/ga)"

    response = (
        f"👤 @{message.from_user.username or message.from_user.id}\n"
        f"📋 Dastlabki xulosa: {assessment}\n\n"
        f"💊 Taklif etilgan vositalar:\n{solutions}\n\n"
        f"{DRAFT_RESPONSE_FOOTER}"
    )

    await message.answer(response)

    # TODO: leadni saqlash va maxsus guruhga yuborish qo'shiladi
