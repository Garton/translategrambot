import logging

from aiogram import F, Router, types

from app.i18n.resources import get_text
from app.keyboards.pairs import popular_pairs_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data.startswith("pair_"))
async def pair_chosen(cb: types.CallbackQuery):
    # save the selected pair in FSM, for now just respond
    reply = await get_text(cb.from_user.language_code, "pair_chosen")
    await cb.message.edit_text(
        reply, reply_markup=None
    )  # edit text and remove keyboard
    await cb.answer()


@router.callback_query(F.data == "choose_pair")
async def pair_choose(cb: types.CallbackQuery):
    await cb.message.answer(
        await get_text(cb.from_user.language_code, "choose_pair"),
        reply_markup=popular_pairs_keyboard(),
    )
