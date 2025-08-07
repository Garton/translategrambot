import pytest

from app.ml.translation_service import TranslationService

ts = TranslationService()


@pytest.mark.asyncio
async def test_ru_en_small():
    out = await ts.translate("Привет, мир", "ru", "en")
    assert "world" in out.lower() or "hello" in out.lower()


@pytest.mark.asyncio
async def test_en_ru_small():
    out = await ts.translate("Hello, world", "en", "ru")
    assert "привет" in out.lower()


@pytest.mark.asyncio
async def test_ru_zh_intermediate():
    """Test Russian to Chinese translation using intermediate method"""
    out = await ts.translate_intermediate("Привет, мир", "ru", "zh")
    assert out is not None
    # Chinese characters should be present in the output
    assert any("\u4e00" <= char <= "\u9fff" for char in out)


@pytest.mark.asyncio
async def test_zh_ru_intermediate():
    """Test Chinese to Russian translation using intermediate method"""
    out = await ts.translate_intermediate("你好，世界", "zh", "ru")
    assert out is not None
    # Russian characters should be present in the output
    assert any("\u0400" <= char <= "\u04ff" for char in out)


@pytest.mark.asyncio
async def test_ru_zh_direct_vs_intermediate():
    """Compare direct translation vs intermediate translation for Russian to Chinese"""
    # Try direct translation first
    direct_out = await ts.translate("Привет, мир", "ru", "zh")

    # Try intermediate translation
    intermediate_out = await ts.translate_intermediate("Привет, мир", "ru", "zh")

    # At least one of them should work
    assert direct_out is not None or intermediate_out is not None

    # If both work, they should be similar (not necessarily identical due to different models)
    if direct_out and intermediate_out:
        # Both should contain Chinese characters
        assert any("\u4e00" <= char <= "\u9fff" for char in direct_out)
        assert any("\u4e00" <= char <= "\u9fff" for char in intermediate_out)
