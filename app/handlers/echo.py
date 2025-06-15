import logging
from aiogram import Router, types, F
from app.ml.language_service import LanguageService
from app.i18m.messages import get_message
from app.keyboards.pairs import popular_pairs_keyboard

logger = logging.getLogger(__name__)
router = Router()
ls = LanguageService()


@router.message()
async def echo(message: types.Message):
    logger.info("%s: %s", message.from_user.id, message.text)

    iso = ls.detect(message.text)
    if iso is None:
        text = get_message(message.from_user.language_code, "unknown")
        await message.answer(text, reply_markup=popular_pairs_keyboard())
        return
    
    await message.answer(f"Translated from {iso}: {message.text}")

@router.callback_query(F.data.startswith("pair_"))
async def pair_chosen(cb: types.CallbackQuery):
    # сохраняем выбранную пару в FSM, пока просто отвечаем
    reply = get_message(cb.from_user.language_code, "pair_chosen")
    await cb.message.edit_reply_markup()   # уберём клаву
    await cb.answer()
    await cb.message.answer(reply)
