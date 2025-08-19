# src/bot/handlers/group.py
from __future__ import annotations

from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from core.constants import ASK_PHOTO_TEXT, ASK_TEXT_INFO, DRAFT_RESPONSE_FOOTER
from core.config import settings

from storage.memory import memory_store
from services.leads import build_lead, save_lead_to_csv, format_lead_for_group
from services.notify import notify_lead_group, notify_admins

router = Router()

def _pick_best_photo_id(message: Message) -> str | None:
    try:
        return message.photo[-1].file_id  # eng katta o'lcham
    except Exception:
        return None

# 1) Faqat matn: rasm so'rash
@router.message(F.text & ~F.photo)
async def handle_text(message: Message):
    # Faqat rasm so'raymiz (suhbatni sodda ushlab turamiz)
    logger.info(f"[GROUP] Faqat matn: {message.from_user.id}")
    await message.reply(ASK_PHOTO_TEXT, reply_to_message_id=message.message_id)

# 2) Faqat rasm: matn so'rash
@router.message(F.photo & ~F.caption)
async def handle_photo(message: Message):
    logger.info(f"[GROUP] Faqat rasm: {message.from_user.id}")
    # Sessiyaga rasmni qo'shib qo'yamiz (kerak bo'lsa)
    fid = _pick_best_photo_id(message)
    if fid:
        memory_store.add_image(chat_id=message.chat.id, user_id=message.from_user.id, file_id=fid)
    await message.reply(ASK_TEXT_INFO, reply_to_message_id=message.message_id)

# 3) Matn + rasm: qisqa xulosa + 1–2 yechim + lead saqlash + report
@router.message(F.photo & F.caption)
async def handle_photo_with_caption(message: Message):
    logger.info(f"[GROUP] Matn+rasm: {message.from_user.id}")

    # --- Dastlabki (dummy) tahlil va yechimlar ---
    assessment = "Trips zararlanishi ehtimoli"
    solutions = [
        "Metomil 90% SP (0.6–0.8 kg/ga)",
        "Spinosad 48% SC (0.2 l/ga)",
    ]

    # Rasm file_id(lar)ini yig'ish
    image_ids = []
    best = _pick_best_photo_id(message)
    if best:
        image_ids.append(best)

    # --- Lead obyektini qurish ---
    lead = build_lead(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        source_chat_id=message.chat.id,
        source_message_id=message.message_id,
        crop=None,                     # Hozircha aniqlamaymiz (DM’da to‘ldiriladi)
        problem_type=None,             # Hozircha aniqlamaymiz
        symptoms_text=message.caption, # Foydalanuvchi yozgani
        bot_assessment=assessment,
        solutions=solutions,
        region=None,                   # DM’da so‘raladi
        contact=None,                  # DM’da so‘raladi
        has_photo=bool(image_ids),
        image_file_ids=image_ids,
        urgency=None,                  # DM’da so‘raladi
    )

    # CSVga saqlash
    try:
        save_lead_to_csv(lead)
    except Exception as e:
        logger.exception(f"Lead CSVga yozishda xatolik: {e}")

    # Maxsus guruhga LEAD-karta yuborish
    try:
        text_for_group = format_lead_for_group(lead)
        # Rasm bo'lsa — caption bilan birga yuboramiz
        await notify_lead_group(
            bot=message.bot,
            text=text_for_group,
            photo_file_ids=image_ids or None,
            report_chat_id=settings.LEAD_REPORT_CHAT_ID,
        )
    except Exception as e:
        logger.exception(f"Lead maxsus guruhga yuborishda xato: {e}")

    # Admin(lar)ga qisqa eslatma
    try:
        await notify_admins(
            bot=message.bot,
            text=f"🧭 Yangi lead: @{message.from_user.username or message.from_user.id} — dastlabki xulosa: {assessment}",
        )
    except Exception as e:
        logger.exception(f"Adminlarga xabar yuborishda xato: {e}")

    # Foydalanuvchiga qisqa javob (guruhda ixcham)
    response = (
        f"👤 @{message.from_user.username or message.from_user.id}\n"
        f"📋 Dastlabki xulosa: {assessment}\n\n"
        f"💊 Taklif etilgan vositalar:\n- {solutions[0]}\n- {solutions[1]}\n\n"
        f"{DRAFT_RESPONSE_FOOTER}"
    )
    await message.reply(response, reply_to_message_id=message.message_id)
