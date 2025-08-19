# src/core/constants.py

START_TEXT = (
    "👋 Salom! Men **Chayla**.\n"
    "Agrar savollaringizga **aniq, ilmiy va zamonaviy** javob beraman, "
    "amaliy yechimlarni taklif qilaman.\n\n"
    "Savolingizni yozing yoki rasm yuboring — holatni baholab, "
    "dunyoda qo‘llaniladigan 1–2 ta mos yechimni ko‘rsataman.\n\n"
    "ℹ️ Bu dastlabki xulosa: yakuniy tavsiya mutaxassis ko‘rib chiqqach beriladi."
)

ASK_PHOTO_TEXT = (
    "📸 Rahmat! Iltimos, kasallangan joyni **yaqin** va **umumiy** ko‘rinishda suratga oling.\n"
    "Rasm qanchalik aniq bo‘lsa, xulosa shunchalik ishonchli bo‘ladi."
)

ASK_TEXT_INFO = (
    "✍️ Iltimos, qisqacha ma’lumot yuboring:\n"
    "- Ekin nomi\n"
    "- Alomatlar (qachondan beri, qaysi qism)\n"
    "- Oxirgi ishlov (dori/doza/sana)\n"
    "- Hudud (viloyat/tuman)"
)

DRAFT_RESPONSE_FOOTER = (
    "⚠️ Bu faqat dastlabki xulosa.\n"
    "Mutaxassis ko‘rib chiqadi va kerak bo‘lsa qo‘shimcha savollar beradi."
)

LEAD_TEMPLATE = (
    "🆕 **LEAD KARTA**\n"
    "👤 Kimdan: {user}\n"
    "🌱 Ekin: {crop}\n"
    "❗ Muammo: {problem}\n"
    "📋 Bot xulosasi: {assessment}\n"
    "💊 Taklif etilgan vositalar: {solutions}\n"
    "📍 Hudud: {region}\n"
    "📞 Aloqa: {contact}\n"
    "🖼️ Rasm: {has_photo}\n"
    "⏱️ Shoshilinchlik: {urgency}"
)
