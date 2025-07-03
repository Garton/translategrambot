# app/keyboards/pairs.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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


def choose_pair_btn(ui_lang: str = "en") -> InlineKeyboardMarkup:
    """
    Single button that opens language-pair selector.
    """
    text = "🔤 Choose languages" if ui_lang == "en" else "🔤 Выбрать языки"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, callback_data="choose_pair")]]
    )
