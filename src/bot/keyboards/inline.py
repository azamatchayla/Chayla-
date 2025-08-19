# src/bot/keyboards/inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Callback data kalitlari
CB_CONFIRM = "lead_confirm"
CB_MORE_INFO = "lead_more_info"
CB_CREATE_ORDER = "lead_create_order"
CB_CONTACT_ADMIN = "lead_contact_admin"

def confirmation_keyboard() -> InlineKeyboardMarkup:
    """
    Xulosa kartasini tasdiqlash yoki qo'shimcha ma'lumot so'rash tugmalari.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=CB_CONFIRM)],
        [InlineKeyboardButton(text="➕ Qo‘shimcha ma’lumot kiritish", callback_data=CB_MORE_INFO)],
    ])

def order_keyboard() -> InlineKeyboardMarkup:
    """
    Buyurtmaga yo'naltiruvchi tugmalar (boshlang'ich bosqich).
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Buyurtma qoldirish", callback_data=CB_CREATE_ORDER)],
        [InlineKeyboardButton(text="👨‍🌾 Adminga yozish", callback_data=CB_CONTACT_ADMIN)],
    ])
