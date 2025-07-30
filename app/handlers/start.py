from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from app.i18n.resources import get_text
from app.keyboards.pairs import choose_pair_btn

router = Router()


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
