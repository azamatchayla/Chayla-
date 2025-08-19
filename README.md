# 🌱 Chayla Bot

Telegram agro-bot — dehqonlarning savollariga ilmiy va zamonaviy javob beradi, 
muammolarni yig‘adi, tavsiyalarni taklif qiladi va sotuvchilar bilan ulaydi.  
**Bitta guruh = bitta bot = bitta katalog.**

---

## 📂 Papka tuzilishi
chayla/
├── src/ # Asosiy kodlar
│ ├── main.py # Polling rejimida ishga tushirish
│ ├── app.py # Webhook rejimida ishga tushirish (Render uchun)
│ ├── core/ # Konfiguratsiya va umumiy kod
│ ├── bot/ # Handlers (private, group) va router
│ └── services/ # AI, leads va boshqa xizmatlar
├── scripts/ # Qo‘shimcha skriptlar (masalan, CSV eksport)
├── infra/ # Deployment fayllar (Dockerfile, render.yaml)
├── requirements.txt # Kutubxonalar ro‘yxati
└── README.md # Hujjat (ushbu fayl)

yaml
Копировать код

---

## ⚙️ O‘rnatish
1. Reponi ko‘chirib oling:
   ```bash
   git clone <repo-link>
   cd chayla
Kutubxonalarni o‘rnating:

bash
Копировать код
pip install -r requirements.txt
.env fayl yarating (yoki Render’da Environment Variables qo‘shing):

ini
Копировать код
TELEGRAM_BOT_TOKEN=your_bot_token
OPENAI_API_KEY=your_openai_key
WEBHOOK_URL=https://your-app.onrender.com/webhook
ADMIN_USER_IDS=123456789
ALLOWED_GROUP_ID=-100123456789
LEAD_REPORT_CHAT_ID=-100987654321
CSV_PATH=/app/leads.csv
🚀 Ishga tushirish
Lokal (polling):
bash
Копировать код
python src/main.py
Server (webhook, Render):
Render avtomatik infra/render.yaml bo‘yicha ishga tushiradi.

📊 Leadlarni olish
Leadlar CSV faylga yoziladi (leads.csv) va maxsus guruhga yuboriladi.
Ekspor qilish uchun:

bash
Копировать код
python scripts/export_csv.py
🛠 Texnologiyalar
Aiogram 3 — Telegram bot framework

FastAPI — Webhook server

OpenAI API — AI javoblari

Pandas — CSV bilan ishlash

✍️ Muallif: Azamat Keldibekov