# app/keyboards/pairs.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

PAIR_BUTTONS = [
    ("RU → EN", "pair_ru_en"),
    ("EN → RU", "pair_en_ru"),
    ("ES → EN", "pair_es_en"),
]

def popular_pairs_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=label, callback_data=data)]
        for label, data in PAIR_BUTTONS
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)
