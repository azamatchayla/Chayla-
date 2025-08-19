# src/storage/csv_store.py
import csv
import os
from typing import Dict, Any, Iterable, List, Optional
from datetime import datetime

from core.config import settings

DEFAULT_HEADERS = [
    "lead_id",
    "created_at",
    "user_id",
    "username",
    "first_name",
    "last_name",
    "source_chat_id",
    "source_message_id",
    "crop",
    "problem_type",
    "symptoms_text",
    "bot_assessment",
    "suggested_products",
    "region",
    "contact",
    "has_photo",
    "image_file_ids",
    "urgency",
    "status",
]

def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"

def _ensure_file(path: str, headers: List[str] = DEFAULT_HEADERS) -> None:
    """CSV fayl mavjud bo'lmasa, sarlavha qatori bilan yaratadi."""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

def append_row(row: Dict[str, Any], path: Optional[str] = None) -> None:
    """Bitta leadni CSV ga qo'shadi (kerakli ustunlarni tartiblaydi)."""
    csv_path = path or settings.CSV_PATH
    _ensure_file(csv_path)

    # Image file ids: list -> ';' bilan birlashtiramiz
    image_ids = row.get("image_file_ids") or []
    if isinstance(image_ids, list):
        image_ids = ";".join(image_ids)

    ordered = [
        str(row.get("lead_id", "")),
        str(row.get("created_at", _now_iso())),
        str(row.get("user_id", "")),
        str(row.get("username", "")),
        str(row.get("first_name", "")),
        str(row.get("last_name", "")),
        str(row.get("source_chat_id", "")),
        str(row.get("source_message_id", "")),
        str(row.get("crop", "")),
        str(row.get("problem_type", "")),
        str(row.get("symptoms_text", "")),
        str(row.get("bot_assessment", "")),
        str(row.get("suggested_products", "")),
        str(row.get("region", "")),
        str(row.get("contact", "")),
        "ha" if row.get("has_photo") else "yo'q",
        image_ids,
        str(row.get("urgency", "")),
        str(row.get("status", "NEW")),
    ]

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(ordered)

def read_all(path: Optional[str] = None) -> List[Dict[str, str]]:
    """CSV dagi barcha leadlarni o‘qib, ro‘yxat ko‘rinishida qaytaradi."""
    csv_path = path or settings.CSV_PATH
    if not os.path.exists(csv_path):
        return []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def filter_by_status(status: str, path: Optional[str] = None) -> List[Dict[str, str]]:
    """Ma'lum statusdagi leadlarni qaytaradi (NEW/CONTACTED/WON/LOST va h.k.)."""
    return [r for r in read_all(path) if r.get("status") == status]

def upsert_status(lead_id: str, new_status: str, path: Optional[str] = None) -> bool:
    """
    lead_id bo'yicha statusni yangilaydi.
    True qaytsa — muvaffaqiyatli, False — topilmadi.
    """
    csv_path = path or settings.CSV_PATH
    if not os.path.exists(csv_path):
        return False

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    found = False
    for r in rows:
        if r.get("lead_id") == lead_id:
            r["status"] = new_status
            found = True
            break

    if not found:
        return False

    # Qayta yozamiz
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=DEFAULT_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    return True
