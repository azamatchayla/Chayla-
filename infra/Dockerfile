# infra/Dockerfile
FROM python:3.11-slim

# OS darajasida ozgina tozalash va tayyorlash
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Talablar
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ilova kodi
COPY src /app/src
COPY scripts /app/scripts
COPY .env.example /app/.env.example
COPY README.md /app/README.md

# CSV fayl uchun (agar kerak bo'lsa) ishchi katalogda yozish oson bo'lsin
VOLUME ["/app"]

# Uvicorn port (Render-da 10000 qulay)
EXPOSE 10000

# Standart start (Render’da baribir Start Command beramiz)
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "10000"]
