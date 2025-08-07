import logging

from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from app.i18n.resources import get_text
from app.keyboards.pairs import choose_pair_btn
from app.services.user_service import UserService

logger = logging.getLogger(__name__)
router = Router()
user_service = UserService()


@router.message(CommandStart())
async def cmd_start(msg: types.Message, state: FSMContext):
    ui_lang = (msg.from_user.language_code or "en")[:2]

    await msg.answer(
        await get_text(ui_lang, "start"),  # <- await !
        reply_markup=choose_pair_btn(ui_lang),
    )


@router.message(Command("help"))
async def cmd_help(msg: types.Message, state: FSMContext):
    ui_lang = (msg.from_user.language_code or "en")[:2]

    await msg.answer(
        await get_text(ui_lang, "help"),  # <- await !
        reply_markup=choose_pair_btn(ui_lang),
    )


@router.message(Command("mypair"))
async def cmd_my_pair(msg: types.Message):
    """Show user's current language pair preference."""
    user_pair = await user_service.get_user_language_pair(msg.from_user.id)

    if user_pair:
        source_lang, target_lang = user_pair
        response = f"🔤 **Your current language pair:**\n{source_lang.upper()} → {target_lang.upper()}"
    else:
        response = "❌ **No language pair set**\nUse /start to choose your preferred language pair."

    await msg.answer(response, parse_mode="Markdown")


@router.message(Command("inline"))
async def cmd_inline(msg: types.Message):
    """Show information about inline mode."""
    ui_lang = (msg.from_user.language_code or "en")[:2]

    inline_help = await get_text(ui_lang, "inline_help")
    await msg.answer(inline_help, parse_mode="Markdown")
