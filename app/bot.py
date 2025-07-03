from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from app.handlers import all_routers

print(f"token: {settings.BOT_TOKEN}")
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

for router in all_routers:
    dp.include_router(router)
