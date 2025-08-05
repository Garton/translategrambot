import logging

from aiogram import F, Router, types

from app.i18n.resources import get_text
from app.keyboards.pairs import get_pair_btn_name, popular_pairs_keyboard
from app.services.user_service import UserService

logger = logging.getLogger(__name__)
router = Router()
user_service = UserService()


@router.callback_query(F.data.startswith("pair_"))
async def pair_chosen(cb: types.CallbackQuery):
    # Extract language pair from callback data (e.g., "pair_en-ru" -> "en-ru")
    pair_data = cb.data.replace("pair_", "")
    source_lang, target_lang = pair_data.split("_", 1)

    # Save user's preferred language pair to database
    await user_service.set_user_language_pair(
        user_id=cb.from_user.id, source_lang=source_lang, target_lang=target_lang
    )

    # Get confirmation message
    reply = await get_text(cb.from_user.language_code, "pair_chosen")
    reply = f"{get_pair_btn_name(cb.data)}: {reply}"
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
