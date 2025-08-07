import asyncio
import logging
from typing import Dict, Optional

from aiogram import F, Router, types
from aiogram.filters import Command

from app.i18n.resources import get_text
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

# Timeout mechanism using inline_query.id
_typing_timeout = 1.0  # Wait 1 second after user stops typing
_user_query_ids: Dict[int, str] = {}  # user_id -> current inline_query.id


@router.inline_query()
async def inline_translate(inline_query: types.InlineQuery):
    """Handle inline queries for translation"""
    query = inline_query.query.strip()
    user_id = inline_query.from_user.id
    current_query_id = inline_query.id

    logger.info(f"Inline query: {query}")

    if not query:
        # Show help message when no query is provided
        help_text = await get_text(inline_query.from_user.language_code, "inline_help")
        await inline_query.answer(
            results=[
                types.InlineQueryResultArticle(
                    id="help",
                    title="Translation Help",
                    input_message_content=types.InputTextMessageContent(
                        message_text=help_text
                    ),
                    description="Send a message to translate it",
                )
            ],
            cache_time=1,
        )
        return

    # Save current query ID for this user
    _user_query_ids[user_id] = current_query_id

    # Sleep for a while to let user finish typing
    await asyncio.sleep(_typing_timeout)

    # Check if query ID has changed (user continued typing)
    if user_id in _user_query_ids and _user_query_ids[user_id] != current_query_id:
        logger.debug(f"Query ID changed for user {user_id}, skipping translation")
        return

    # Detect source language
    src_iso_detected = ls.detect(query)
    src_iso = src_iso_detected
    target_iso = None
    user_pair = await user_service.get_user_language_pair(inline_query.from_user.id)
    if user_pair:
        src_iso, target_iso = user_pair

    if src_iso is None:
        error_text = await get_text(inline_query.from_user.language_code, "unknown")
        await inline_query.answer(
            results=[
                types.InlineQueryResultArticle(
                    id="error",
                    title="Language Detection Failed",
                    input_message_content=types.InputTextMessageContent(
                        message_text=error_text
                    ),
                    description="Could not detect the language",
                )
            ],
            cache_time=1,
        )
        return

    # Extract target language from query
    extracted_target_iso, text = extract_target_language(query)
    if extracted_target_iso:
        target_iso = extracted_target_iso

    if target_iso and target_iso == src_iso:
        if src_iso_detected and src_iso_detected != src_iso:
            src_iso = src_iso_detected
        else:
            # Same language, just return the text
            await inline_query.answer(
                results=[
                    types.InlineQueryResultArticle(
                        id="same_lang",
                        title="Same Language",
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"This is the same language ({src_iso}):\n\n{text}"
                        ),
                        description=f"Text is already in {src_iso}",
                    )
                ],
                cache_time=1,
            )
            return

    # Try to translate
    translated = await translator.translate_intermediate(text, src_iso, target_iso)

    if translated:
        # Save user's language pair preference
        await user_service.set_user_language_pair(
            inline_query.from_user.id, src_iso, target_iso
        )

        # Create result with translated text
        await inline_query.answer(
            results=[
                types.InlineQueryResultArticle(
                    id="translation",
                    title=f"Translation ({src_iso} → {target_iso})",
                    input_message_content=types.InputTextMessageContent(
                        message_text=translated
                    ),
                    description=translated,
                )
            ],
            cache_time=1,
        )
    else:
        # Try intermediate translation
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
                # Save user's language pair preference
                await user_service.set_user_language_pair(
                    inline_query.from_user.id, src_iso, target_iso
                )

                await inline_query.answer(
                    results=[
                        types.InlineQueryResultArticle(
                            id="translation_intermediate",
                            title=f"Translation via {DEFAULT_INTERMEDIATE_LANGUAGE} ({src_iso} → {target_iso})",
                            input_message_content=types.InputTextMessageContent(
                                message_text=f"🌐 **Translation** ({src_iso} → {target_iso} via {DEFAULT_INTERMEDIATE_LANGUAGE})\n\n"
                                f"**Original:** {text}\n\n"
                                f"**Translated:** {translated}"
                            ),
                            description=f"Translate from {src_iso} to {target_iso} via {DEFAULT_INTERMEDIATE_LANGUAGE}",
                        )
                    ],
                    cache_time=1,
                )
                return

        # Translation failed
        error_text = await get_text(
            inline_query.from_user.language_code, "translation_failed"
        )
        await inline_query.answer(
            results=[
                types.InlineQueryResultArticle(
                    id="translation_failed",
                    title="Translation Failed",
                    input_message_content=types.InputTextMessageContent(
                        message_text=f"❌ {error_text}\n\n**Text:** {text}\n**From:** {src_iso}\n**To:** {target_iso}"
                    ),
                    description="Could not translate the text",
                )
            ],
            cache_time=1,
        )


@router.chosen_inline_result()
async def chosen_inline_result(chosen_result: types.ChosenInlineResult):
    """Handle when user selects an inline result"""
    logger.info(
        f"User {chosen_result.from_user.id} selected inline result: {chosen_result.result_id}"
    )
    # You can add additional logging or analytics here if needed
