import asyncio

import pytest

from app.ml.translation_service import TranslationService

ts = TranslationService()


@pytest.mark.asyncio
async def test_ru_en_small():
    out = await ts.translate("Привет, мир", "ru", "en")
    assert "world" in out.lower()


@pytest.mark.asyncio
async def test_en_ru_small():
    out = await ts.translate("Hello, world", "en", "ru")
    assert "привет" in out.lower()
