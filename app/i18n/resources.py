# app/i18n/resources.py
"""
Runtime i18n strings.  Fallback text is auto-translated and cached.
"""
from app.i18n.base_texts import TEXTS
from app.services import translation_service

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
