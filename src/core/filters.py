from aiogram.filters import BaseFilter
from aiogram.types import Message
from core.config import settings


class AllowedGroupFilter(BaseFilter):
    """
    Faqat ruxsat etilgan guruhda ishlash filtri.
    """
    async def __call__(self, message: Message) -> bool:
        # Guruh emas (private chat) bo'lsa ham ruxsat beramiz
        if message.chat.type == "private":
            return True

        # Guruh bo'lsa, faqat ALLOWED_GROUP_ID ga ruxsat beramiz
        return message.chat.id == settings.ALLOWED_GROUP_ID
