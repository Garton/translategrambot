import re

LANGUAGES = {
    "английский": "en",
    "русский": "ru",
    "китайский": "zh",
    "французский": "fr",
    "немецкий": "de",
    "испанский": "es",
    "итальянский": "it",
}


def extract_target_language(text: str) -> str:
    pattern = r"переведи на (\w+)"
    match = re.search(pattern, text.lower())
    full_russian_name = match.group(1) if match else None
    language = LANGUAGES.get(full_russian_name.lower(), None)
    if match:
        text = text.replace(match.group(0), "")
    return (language, text)
