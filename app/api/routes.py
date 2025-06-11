from fastapi import APIRouter, Request
from app.bot import dp, bot

router = APIRouter()

@router.post("/webhook")
async def telegram_webhook(request: Request):
    update = await request.body()
    await dp.feed_raw_update(bot, update)
    return {"status": "ok"}
