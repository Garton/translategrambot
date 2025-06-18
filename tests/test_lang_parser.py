import pytest

from app.ml.language_parser import extract_target_language


@pytest.mark.parametrize(
    "test, expected",
    [
        ("переведи на русский", "ru"),
        ("переведи на английский", "en"),
        ("переведи на немецкий, пожалуйста", "de"),
        ("переведи на французский, пожалуйста", "fr"),
        ("переведи на испанский, пожалуйста", "es"),
    ],
)
def test_extract_target_language(test, expected):
    assert extract_target_language(test)[0] == expected
