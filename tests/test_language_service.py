import pytest

from app.ml.language_service import LanguageService

lang_service = LanguageService()


@pytest.mark.parametrize(
    "txt, iso",
    [
        # English cases
        ("hello", None),
        ("Good day mr. Smith", "en"),
        ("The quick brown fox jumps over the lazy dog", "en"),
        # Russian cases
        ("привет", None),
        ("привет, мой дорогой друг", "ru"),
        ("Москва - столица России", "ru"),
        # Spanish case
        ("Hola, ¿cómo estás?", "es"),
        # Emoji case
        ("Hello 👋", None),  # emoji should not affect detection
        # Empty and invalid cases
        ("     ", None),
        ("", None),
        ("123", None),
    ],
)
def test_detect(txt, iso):
    assert lang_service.detect(txt) == iso
