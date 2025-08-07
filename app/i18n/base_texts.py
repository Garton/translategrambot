from typing import Dict

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
            "• Or press the button below to pick languages.\n"
            "• Use /inline for inline mode in other chats.\n\n"
            "*Supported languages*: English, Russian, German, French, "
            "Spanish, Italian, Chinese, You name it!"
        ),
        # /reset or end of session
        "bye": "👋 Settings cleared. Type /start to begin again.",
        "pair_chosen": "Great! Now send the text to translate.",
        "choose_pair": "🔤 Choose source → target language:",
        "unknown_language_pair": "🙏 We are sorry, but we are not able to figure out this language pair",
        "inline_help": (
            "🌐 *Inline Translation*\n\n"
            "To use inline translation:\n"
            "1. Type @YourBotName in any chat\n"
            "2. Add the text you want to translate\n"
            "3. Optionally specify target language: `text @en` for English\n"
            "4. Select the translation result\n\n"
            "Example: `Hello world @ru` to translate to Russian"
        ),
        "translation_failed": "Translation failed. Please try a different language pair.",
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
            "• Или нажмите кнопку выбора языков.\n"
            "• Используйте /inline для инлайн режима в других чатах.\n\n"
            "*Поддерживаемые языки*: английский, русский, немецкий, "
            "французский, испанский, итальянский, китайский, и все остальные!"
        ),
        "bye": "👋 Настройки сброшены. Наберите /start, чтобы начать заново.",
        "pair_chosen": "Отлично! Теперь отправьте текст для перевода.",
        "choose_pair": "🔤 Выберите направление перевода:",
        "unknown_language_pair": "🙏 Мы очень сожалеем, но не можем определить пару языков",
        "inline_help": (
            "🌐 *Инлайн перевод*\n\n"
            "Чтобы использовать инлайн перевод:\n"
            "1. Введите @YourBotName в любом чате\n"
            "2. Добавьте текст для перевода\n"
            "3. Опционально укажите язык: `текст @en` для английского\n"
            "4. Выберите результат перевода\n\n"
            "Пример: `Привет мир @en` для перевода на английский"
        ),
        "translation_failed": "Перевод не удался. Попробуйте другую пару языков.",
    },
}
