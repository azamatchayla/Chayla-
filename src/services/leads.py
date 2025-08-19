# src/services/leads.py
import csv
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from core.config import settings
from core.constants import LEAD_TEMPLATE

CSV_HEADERS = [
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


def _ensure_csv_exists(path: str) -> None:
    """CSV fayl mavjud bo'lmasa, sarlavhalar bilan yaratadi."""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)


def _to_csv_row(lead: Dict[str, Any]) -> List[str]:
    """Lead obyektini CSV qatoriga aylantirish (tartib CSV_HEADERS bo‘yicha)."""
    # list -> ';' bilan birlashtiramiz
    image_ids = lead.get("image_file_ids") or []
    if isinstance(image_ids, list):
        image_ids = ";".join(image_ids)

    return [
        str(lead.get("lead_id", "")),
        str(lead.get("created_at", "")),
        str(lead.get("user_id", "")),
        str(lead.get("username", "")),
        str(lead.get("first_name", "")),
        str(lead.get("last_name", "")),
        str(lead.get("source_chat_id", "")),
        str(lead.get("source_message_id", "")),
        str(lead.get("crop", "")),
        str(lead.get("problem_type", "")),
        str(lead.get("symptoms_text", "")),
        str(lead.get("bot_assessment", "")),
        str(lead.get("suggested_products", "")),  # "Prod A | Prod B" ko'rinishida
        str(lead.get("region", "")),
        str(lead.get("contact", "")),
        "ha" if lead.get("has_photo") else "yo'q",
        image_ids,
        str(lead.get("urgency", "")),
        str(lead.get("status", "NEW")),
    ]


def build_lead(
    *,
    user_id: int,
    username: Optional[str],
    first_name: Optional[str],
    last_name: Optional[str],
    source_chat_id: int,
    source_message_id: int,
    crop: Optional[str],
    problem_type: Optional[str],
    symptoms_text: Optional[str],
    bot_assessment: str,
    solutions: List[str],
    region: Optional[str],
    contact: Optional[str],
    has_photo: bool,
    image_file_ids: Optional[List[str]] = None,
    urgency: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Kiruvchi ma'lumotlardan lead obyektini quradi.
    solutions: ["Metomil 90% SP (0.6–0.8 kg/ga)", "Spinosad 48% SC (0.2 l/ga)"]
    """
    lead_id = f"L{int(datetime.utcnow().timestamp())}{user_id}"
    suggested_products = " | ".join(solutions[:2]) if solutions else ""

    lead = {
        "lead_id": lead_id,
        "created_at": _now_iso(),
        "user_id": user_id,
        "username": username or "",
        "first_name": first_name or "",
        "last_name": last_name or "",
        "source_chat_id": source_chat_id,
        "source_message_id": source_message_id,
        "crop": (crop or "").strip(),
        "problem_type": (problem_type or "").strip(),
        "symptoms_text": (symptoms_text or "").strip(),
        "bot_assessment": (bot_assessment or "").strip(),
        "suggested_products": suggested_products,
        "region": (region or "").strip(),
        "contact": (contact or "").strip(),
        "has_photo": bool(has_photo),
        "image_file_ids": image_file_ids or [],
        "urgency": (urgency or "").strip(),  # "bugun" / "24 soat" / "3 kun"
        "status": "NEW",
    }
    return lead


def save_lead_to_csv(lead: Dict[str, Any], path: Optional[str] = None) -> None:
    """
    Leadni CSV faylga yozadi. Fayl bo'lmasa sarlavha bilan yaratadi.
    """
    csv_path = path or settings.CSV_PATH
    _ensure_csv_exists(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(_to_csv_row(lead))


def format_lead_for_group(lead: Dict[str, Any]) -> str:
    """
    Maxsus guruhga yuborish uchun LEAD matnini tayyorlaydi (LEAD_TEMPLATE asosida).
    """
    user_disp = (
        f"@{lead['username']}" if lead.get("username")
        else f"ID:{lead.get('user_id')}"
    )
    has_photo_text = "ha" if lead.get("has_photo") else "yo‘q"

    txt = LEAD_TEMPLATE.format(
        user=user_disp,
        crop=lead.get("crop") or "—",
        problem=lead.get("problem_type") or (lead.get("symptoms_text") or "—"),
        assessment=lead.get("bot_assessment") or "—",
        solutions=lead.get("suggested_products") or "—",
        region=lead.get("region") or "—",
        contact=lead.get("contact") or "DM",
        has_photo=has_photo_text,
        urgency=lead.get("urgency") or "—",
    )
    return txt
