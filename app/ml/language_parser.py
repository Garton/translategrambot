import re


def extract_target_language(text: str) -> str:
    pattern = r"переведи на (\w+)"
    match = re.search(pattern, text.lower())
    return match.group(1) if match else None
