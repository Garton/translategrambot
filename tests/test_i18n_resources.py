from unittest.mock import AsyncMock, patch

import pytest

from app.i18n.resources import DEFAULT_LANG, TEXTS, get_text


@pytest.mark.asyncio
async def test_get_text_existing_english():
    """Test getting existing English text"""
    result = await get_text("en", "start")
    assert result == TEXTS["en"]["start"]
    assert "universal translator bot" in result


@pytest.mark.asyncio
async def test_get_text_existing_russian():
    """Test getting existing Russian text"""
    result = await get_text("ru", "start")
    assert result == TEXTS["ru"]["start"]
    assert "универсальный переводчик" in result


@pytest.mark.asyncio
async def test_get_text_default_language():
    """Test getting text with None language (should use default)"""
    result = await get_text(None, "start")
    assert result == TEXTS[DEFAULT_LANG]["start"]


@pytest.mark.asyncio
async def test_get_text_language_code_truncation():
    """Test that language codes are truncated to 2 characters"""
    result = await get_text("en-US", "start")
    assert result == TEXTS["en"]["start"]


@pytest.mark.asyncio
async def test_get_text_fallback_translation():
    """Test fallback translation when text doesn't exist in target language"""
    with patch("app.i18n.resources.translation_service") as mock_translation:
        mock_translation.translate = AsyncMock(return_value="Translated text")

        # Test with a language that doesn't have the "start" text
        result = await get_text("fr", "start")

        # Should call translation service
        mock_translation.translate.assert_called_once_with(
            TEXTS[DEFAULT_LANG]["start"], DEFAULT_LANG, "fr"
        )
        assert result == "Translated text"


@pytest.mark.asyncio
async def test_get_text_fallback_translation_caching():
    """Test that translated text is cached after first translation"""
    with patch("app.i18n.resources.translation_service") as mock_translation:
        mock_translation.translate = AsyncMock(return_value="Cached translated text")

        # First call should translate
        result1 = await get_text("de", "start")
        assert result1 == "Cached translated text"
        assert mock_translation.translate.call_count == 1

        # Second call should use cached version
        result2 = await get_text("de", "start")
        assert result2 == "Cached translated text"
        assert mock_translation.translate.call_count == 1  # No additional calls


@pytest.mark.asyncio
async def test_get_text_translation_failure():
    """Test fallback to English when translation fails"""
    with patch("app.i18n.resources.translation_service") as mock_translation:
        mock_translation.translate = AsyncMock(return_value=None)

        result = await get_text("es", "start")

        # Should fallback to English text
        assert result == TEXTS[DEFAULT_LANG]["start"]


@pytest.mark.asyncio
async def test_get_text_all_keys():
    """Test all available keys work correctly"""
    keys = ["start", "choose_pair", "pair_chosen", "unknown", "help", "bye"]

    for key in keys:
        result = await get_text("en", key)
        assert result == TEXTS["en"][key]
        assert result is not None
        assert len(result) > 0


@pytest.mark.asyncio
async def test_get_text_nonexistent_key():
    """Test behavior with non-existent key"""
    with pytest.raises(KeyError):
        await get_text("fr", "nonexistent_key")
