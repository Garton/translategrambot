from app.bot import bot
from app.core.config import settings


async def register_webhook():
    await bot.set_webhook(url=f"{settings.WEBHOOK_URL}/webhook")
