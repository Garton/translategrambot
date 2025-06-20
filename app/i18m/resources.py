# app/i18n/resources.py
"""
Runtime i18n strings.  Fallback text is auto-translated and cached.
"""
from typing import Dict

from app.services import translation_service

TEXTS: Dict[str, Dict[str, str]] = {
    "en": {
        # Sent after /start
        "start": (
            "👋 *Hi!* I’m a *universal translator bot*.\n\n"
            "➊ I automatically detect the language you write in.\n"
            "➋ I translate it to the *target* language.\n\n"
            "➡️ *How to begin*\n"
            "• Press **“Choose languages”** below and pick a pair, **or**\n"
            "• Simply write: `translate to German Hello, friend!`"
        ),
        # "Choose languages" button
        "choose_pair": "🔤 Choose source → target language:",
        # Response after choosing a pair
        "pair_chosen": "✅ Great! Now send the text you want to translate.",
        # When detect == None
        "unknown": (
            "🤔 Sorry, I couldn't detect the language.\n"
            "Please send a longer text or specify a target language, e.g. "
            "`translate to English …`"
        ),
        # Help
        "help": (
            "📖 *Usage*\n"
            "• Type a message with `translate to <language>` inside.\n"
            "• Or press the button below to pick languages.\n\n"
            "*Supported languages*: English, Russian, German, French, "
            "Spanish, Italian, Chinese."
        ),
        # /reset or end of session
        "bye": "👋 Settings cleared. Type /start to begin again.",
    },
    "ru": {
        "start": (
            "👋 *Привет!* Я *универсальный переводчик*.\n\n"
            "➊ Автоматически определяю язык вашего сообщения.\n"
            "➋ Перевожу его на *целевой* язык.\n\n"
            "➡️ *Как начать*\n"
            "• Нажмите **«Выбрать языки»** ниже и задайте пару, **или**\n"
            "• Просто напишите: `переведи на немецкий Привет, друг!`"
        ),
        "choose_pair": "🔤 Выберите направление перевода:",
        "pair_chosen": "✅ Отлично! Отправьте текст для перевода.",
        "unknown": (
            "🤔 Не удалось определить язык.\n"
            "Пришлите более длинный текст или явно укажите язык, "
            "например: `переведи на английский …`"
        ),
        "help": (
            "📖 *Как пользоваться*\n"
            "• Добавьте в сообщение `переведи на <язык>`.\n"
            "• Или нажмите кнопку выбора языков.\n\n"
            "*Поддерживаемые языки*: английский, русский, немецкий, "
            "французский, испанский, итальянский, китайский."
        ),
        "bye": "👋 Настройки сброшены. Наберите /start, чтобы начать заново.",
    },
}

DEFAULT_LANG = "en"


async def get_text(lang: str | None, key: str) -> str:
    """
    Return UI string for given language.
    If missing — translate from English via TranslationService.
    """
    base = TEXTS.get(lang := (lang or DEFAULT_LANG)[:2])
    if base and key in base:
        return base[key]

    # fallback: translate English text, cache it
    src_text = TEXTS[DEFAULT_LANG][key]
    translated = await translation_service.translate(src_text, DEFAULT_LANG, lang)
    if translated:
        TEXTS.setdefault(lang, {})[key] = translated
        return translated

    # last resort — English
    return src_text
