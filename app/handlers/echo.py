from aiogram import Router, types
from app.ml.language_parser import extract_target_language

import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message()
async def echo(message: types.Message):
    logger.info("%s: %s", message.from_user.id, message.text)
    target_language = extract_target_language(message.text)
    if target_language:
        await message.answer(f"Translated to {target_language}: {message.text}")
    else:
        await message.answer("I don't understand you")
