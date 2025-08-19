# scripts/export_csv.py
"""
Lead bazasini CSV formatida eksport qilish skripti.
Terminaldan alohida chaqiriladi:

    python scripts/export_csv.py
"""

import os
import csv
from datetime import datetime
from pathlib import Path

from core.config import settings

LEADS_DIR = Path(settings.LEADS_CSV_PATH).parent

def export_all_leads():
    """
    Leads.csv faylini vaqt belgisi bilan nusxa qiladi.
    """
    src = Path(settings.LEADS_CSV_PATH)
    if not src.exists():
        print(f"[!] {src} topilmadi. Hali hech qanday lead saqlanmagan.")
        return None

    LEADS_DIR.mkdir(parents=True, exist_ok=True)

    # Yangi nom: leads_2025-08-19_120000.csv
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    dest = LEADS_DIR / f"leads_{timestamp}.csv"

    with open(src, "r", encoding="utf-8") as f_in, open(dest, "w", newline="", encoding="utf-8") as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        for row in reader:
            writer.writerow(row)

    print(f"[ok] Leadlar '{dest}' fayliga eksport qilindi.")
    return dest


if __name__ == "__main__":
    export_all_leads()
