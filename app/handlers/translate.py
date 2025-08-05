import logging

from aiogram import F, Router, types

from app.i18n.resources import get_text
from app.keyboards.pairs import popular_pairs_keyboard
from app.ml.language_parser import extract_target_language
from app.ml.language_service import LanguageService
from app.ml.translation_service import TranslationService
from app.services.user_service import UserService

logger = logging.getLogger(__name__)
router = Router()
ls = LanguageService()
translator = TranslationService()
user_service = UserService()

DEFAULT_INTERMEDIATE_LANGUAGE = "en"


@router.message()
async def translate(message: types.Message):
    logger.info("%s: %s", message.from_user.id, message.text)

    text = message.text or ""
    src_iso = ls.detect(message.text)

    user_pair = await user_service.get_user_language_pair(message.from_user.id)

    if src_iso is None and user_pair is None:
        text = await get_text(message.from_user.language_code, "unknown")
        await message.answer(text, reply_markup=popular_pairs_keyboard())
        return

    target_iso, text = extract_target_language(text)

    # If no target language specified in message, try to use user's stored preference
    if not target_iso and user_pair:
        src_iso, target_iso = user_pair

    if target_iso and target_iso == src_iso:
        await message.answer("This is the same language...")
        await message.answer(text)
        return

    if target_iso:
        await user_service.set_user_language_pair(
            message.from_user.id, src_iso, target_iso
        )

        translated = await translator.translate(text, src_iso, target_iso)
        if translated:
            await message.answer(translated)
            return
        else:  # trying use intermediate language
            logger.info(
                f"Failed to translate language {src_iso} to {target_iso}, trying intermediate language {DEFAULT_INTERMEDIATE_LANGUAGE}"
            )
            translated_intermediate = await translator.translate(
                text, src_iso, DEFAULT_INTERMEDIATE_LANGUAGE
            )
            if translated_intermediate:
                translated = await translator.translate(
                    translated_intermediate, DEFAULT_INTERMEDIATE_LANGUAGE, target_iso
                )
                if translated:
                    await message.answer(translated)
                    return
            else:
                logger.info(
                    f"Failed to translate language {src_iso} through intermediate language {DEFAULT_INTERMEDIATE_LANGUAGE} to {target_iso}"
                )

    unknown_pair_text = await get_text(
        message.from_user.language_code, "unknown_language_pair"
    )
    await message.answer(unknown_pair_text, reply_markup=popular_pairs_keyboard())
