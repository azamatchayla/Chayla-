# src/storage/memory.py
from __future__ import annotations
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field
from time import time

DEFAULT_TTL = 60 * 60  # 1 soat: vaqtinchalik kontekstlar uchun

@dataclass
class SessionData:
    """
    Bitta foydalanuvchi yoki bitta muloqot konteksti uchun vaqtinchalik ma'lumotlar.
    """
    user_id: int
    chat_id: int
    last_message_id: Optional[int] = None

    # Intake uchun to'planadigan ma'lumotlar
    crop: Optional[str] = None
    problem_type: Optional[str] = None
    symptoms_text: Optional[str] = None
    region: Optional[str] = None
    contact: Optional[str] = None
    urgency: Optional[str] = None

    # Media
    image_file_ids: List[str] = field(default_factory=list)

    # Boshqa
    extras: Dict[str, Any] = field(default_factory=dict)
    updated_at: float = field(default_factory=time)

    def touch(self) -> None:
        self.updated_at = time()


class MemoryStore:
    """
    Oddiy in-memory session/kontekst saqlagich.
    Keyinchalik Redis/DB ga oson ko'chirish uchun minimal API.
    """
    def __init__(self, ttl_seconds: int = DEFAULT_TTL) -> None:
        self._data: Dict[str, SessionData] = {}
        self._ttl = ttl_seconds

    def _key(self, chat_id: int, user_id: int) -> str:
        return f"{chat_id}:{user_id}"

    def get(self, chat_id: int, user_id: int) -> Optional[SessionData]:
        key = self._key(chat_id, user_id)
        sess = self._data.get(key)
        if not sess:
            return None
        # TTL tekshiruvi
        if time() - sess.updated_at > self._ttl:
            self.delete(chat_id, user_id)
            return None
        return sess

    def get_or_create(self, chat_id: int, user_id: int) -> SessionData:
        sess = self.get(chat_id, user_id)
        if sess:
            return sess
        key = self._key(chat_id, user_id)
        sess = SessionData(user_id=user_id, chat_id=chat_id)
        self._data[key] = sess
        return sess

    def update(
        self,
        chat_id: int,
        user_id: int,
        **fields: Any,
    ) -> SessionData:
        sess = self.get_or_create(chat_id, user_id)
        for k, v in fields.items():
            if hasattr(sess, k):
                setattr(sess, k, v)
            else:
                sess.extras[k] = v
        sess.touch()
        return sess

    def add_image(self, chat_id: int, user_id: int, file_id: str) -> SessionData:
        sess = self.get_or_create(chat_id, user_id)
        if file_id and file_id not in sess.image_file_ids:
            sess.image_file_ids.append(file_id)
        sess.touch()
        return sess

    def delete(self, chat_id: int, user_id: int) -> None:
        key = self._key(chat_id, user_id)
        if key in self._data:
            del self._data[key]

    def clear_expired(self) -> int:
        """
        TTL o'tgan sessiyalarni tozalaydi. Qancha o'chirilganini qaytaradi.
        """
        now = time()
        to_delete = [k for k, s in self._data.items() if now - s.updated_at > self._ttl]
        for k in to_delete:
            del self._data[k]
        return len(to_delete)


# Global store instantsi (oddiy holatda bitta jarayon ichida yetarli)
memory_store = MemoryStore()
