import logging
from aiogram import Router, types, F
from app.ml.language_service import LanguageService
from app.ml.translation_service import TranslationService
from app.ml.language_parser import extract_target_language
from app.i18m.messages import get_message
from app.keyboards.pairs import popular_pairs_keyboard

logger = logging.getLogger(__name__)
router = Router()
ls = LanguageService()
translator = TranslationService()


@router.message()
async def echo(message: types.Message):
    logger.info("%s: %s", message.from_user.id, message.text)

    text = message.text or ""
    src_iso = ls.detect(message.text)
    if src_iso is None:
        text = get_message(message.from_user.language_code, "unknown")
        await message.answer(text, reply_markup=popular_pairs_keyboard())
        return
    
    target_iso = extract_target_language(message.text)
    if target_iso and target_iso == src_iso:
        await message.answer("This is the same language...")
        await message.answer(text)
        return
    
    if target_iso:
        translated = await translator.translate(
            text,
            src_iso,
            target_iso
        )
        if translated:
            await message.answer(translated)
            return

    await message.answer("Unknown language pair")


@router.callback_query(F.data.startswith("pair_"))
async def pair_chosen(cb: types.CallbackQuery):
    # сохраняем выбранную пару в FSM, пока просто отвечаем
    reply = get_message(cb.from_user.language_code, "pair_chosen")
    await cb.message.edit_reply_markup()   # уберём клаву
    await cb.answer()
    await cb.message.answer(reply)
