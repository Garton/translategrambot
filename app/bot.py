from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from app.handlers import all_routers

print(f"token: {settings.BOT_TOKEN}")

# Configure session with better timeout settings
session = AiohttpSession(
    timeout=30.0,  # Reduce timeout from default 60s to 30s
)

bot = Bot(token=settings.BOT_TOKEN, session=session)
dp = Dispatcher(storage=MemoryStorage())

for router in all_routers:
    dp.include_router(router)
