from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from app.handlers.echo import router as echo_router

print(f"token: {settings.BOT_TOKEN}")
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(echo_router)
