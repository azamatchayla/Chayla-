# src/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    ALLOWED_GROUP_ID: int
    ADMIN_USER_IDS: str = ""           # "123,456" ko'rinishida
    LEAD_REPORT_CHAT_ID: int

    # Webhook (serverda ishlaganda)
    WEBHOOK_URL: str | None = None     # Renderda beriladi (https://.../webhook)

    # Saqlash (hozircha CSV)
    STORAGE_BACKEND: str = "csv"       # "csv" | keyin DB/Sheets bo'lishi mumkin
    CSV_PATH: str = "./leads.csv"

    # AI (ixtiyoriy, keyin ishlatamiz)
    OPENAI_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",               # lokal sinovda .env'dan oladi
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

# Global settings obyektini yaratib qo'yamiz
settings = Settings()
