import logging

from aiogram import F, Router, types

from app.i18n.resources import get_text
from app.keyboards.pairs import popular_pairs_keyboard
from app.ml.language_parser import extract_target_language
from app.ml.language_service import LanguageService
from app.ml.translation_service import TranslationService

logger = logging.getLogger(__name__)
router = Router()
ls = LanguageService()
translator = TranslationService()


@router.message()
async def translate(message: types.Message):
    logger.info("%s: %s", message.from_user.id, message.text)

    text = message.text or ""
    src_iso = ls.detect(message.text)
    if src_iso is None:
        text = await get_text(message.from_user.language_code, "unknown")
        await message.answer(text, reply_markup=popular_pairs_keyboard())
        return

    target_iso, text = extract_target_language(text)
    if target_iso and target_iso == src_iso:
        await message.answer("This is the same language...")
        await message.answer(text)
        return

    if target_iso:
        translated = await translator.translate(text, src_iso, target_iso)
        if translated:
            await message.answer(translated)
            return

    await message.answer("Unknown language pair")
