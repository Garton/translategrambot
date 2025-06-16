from aiogram.types import Update
from fastapi import APIRouter, Request

from app.bot import bot, dp

router = APIRouter()


@router.post("/webhook")
async def telegram_webhook(request: Request):
    body = await request.json()
    update = Update.model_validate(body)
    await dp.feed_update(bot, update)
    return {"status": "ok"}
