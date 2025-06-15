import pytest
from app.ml.language_service import LanguageService

lang_service = LanguageService()

@pytest.mark.parametrize(
        "txt, iso",
        [
            ("hello", None),
            ("Good day mr. Smith", "en"),
            ("привет", None),
            ("привет, мой дорогой друг", "ru"),
            ("     ", None),
            ("", None),
            ("123", None),
            ("123", None),
        ],
)
def test_detect(txt, iso):
    assert lang_service.detect(txt) == iso
