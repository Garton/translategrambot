import re
from typing import Optional, Tuple

from app.i18n.languages import LANGUAGES_EN, LANGUAGES_RU

# common trigger phrases
TRIGGER_RGX = re.compile(
    r"(?:переведи(?:те)?\s+на|translate\s+to|@)\s*([a-zA-Zа-яё]+)",
    re.I,
)


def extract_target_language(text: str) -> Tuple[Optional[str], str]:
    """
    Detects 'translate to <lang>' / 'переведи на <язык>'.
    Returns (ISO-2 target or None, cleaned_text).
    """
    m = TRIGGER_RGX.search(text)
    if not m:
        return None, text

    lang_token = m.group(1).lower()
    tgt = LANGUAGES_RU.get(lang_token) or LANGUAGES_EN.get(lang_token)

    cleaned = text.replace(m.group(0), "").strip()
    return tgt, cleaned
