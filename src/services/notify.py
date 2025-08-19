# src/services/notify.py
from typing import Iterable, List, Optional

from aiogram import Bot
from aiogram.types import InputMediaPhoto
from loguru import logger

from core.config import settings

def _parse_admin_ids() -> List[int]:
    raw = (settings.ADMIN_USER_IDS or "").strip()
    if not raw:
        return []
    ids = []
    for p in raw.split(","):
        p = p.strip()
        if not p:
            continue
        try:
            ids.append(int(p))
        except ValueError:
            logger.warning(f"ADMIN_USER_IDS ichida noto'g'ri ID: {p}")
    return ids

async def notify_lead_group(
    bot: Bot,
    text: str,
    photo_file_ids: Optional[Iterable[str]] = None,
    report_chat_id: Optional[int] = None,
) -> None:
    """
    Lead-karta matnini maxsus guruhga yuboradi.
    Agar bir nechta rasm bo'lsa, birinchisini caption bilan yuboradi.
    """
    chat_id = report_chat_id or settings.LEAD_REPORT_CHAT_ID
    photos = list(photo_file_ids or [])

    try:
        if photos:
            if len(photos) == 1:
                await bot.send_photo(chat_id=chat_id, photo=photos[0], caption=text)
            else:
                media = [InputMediaPhoto(media=photos[0], caption=text)]
                for fid in photos[1:]:
                    media.append(InputMediaPhoto(media=fid))
                await bot.send_media_group(chat_id=chat_id, media=media)
        else:
            await bot.send_message(chat_id=chat_id, text=text)
        logger.info(f"Lead maxsus guruhga yuborildi: {chat_id}")
    except Exception as e:
        logger.exception(f"Lead-ni maxsus guruhga yuborishda xato: {e}")

async def notify_admins(bot: Bot, text: str) -> None:
    """
    Admin(lar)ga oddiy matn yuboradi.
    """
    admin_ids = _parse_admin_ids()
    for admin_id in admin_ids:
        try:
            await bot.send_message(chat_id=admin_id, text=text)
        except Exception as e:
            logger.exception(f"Admin {admin_id} ga xabar yuborishda xato: {e}")
