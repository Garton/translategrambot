import pytest

from app.ml.language_parser import extract_target_language


@pytest.mark.parametrize(
    "test, expected",
    [
        ("переведи на русский", "русский"),
        ("переведи на английский", "английский"),
        ("переведи на немецкий, пожалуйста", "немецкий"),
        ("переведи на французский, пожалуйста", "французский"),
        ("переведи на испанский, пожалуйста", "испанский"),
    ]
)
def test_extract_target_language(test, expected):
    assert extract_target_language(test) == expected