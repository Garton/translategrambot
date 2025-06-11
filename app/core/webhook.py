from app.core.config import settings
from app.bot import bot

async def register_webhook():
    await bot.set_webhook(url=f"{settings.WEBHOOK_URL}/webhook")
