import asyncio
import logging
from typing import Optional

from fastapi import FastAPI

from app.api.routes import router
from app.bot import bot, dp
from app.core.webhook import register_webhook
from app.logging_conf import setup_logging
from app.services.message_filter import discard_old_updates

setup_logging()
logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(router)


async def retry_with_backoff(func, max_retries: int = 3, base_delay: float = 1.0):
    """Retry function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} attempts: {e}")
                raise
            delay = base_delay * (2**attempt)
            logger.warning(
                f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s..."
            )
            await asyncio.sleep(delay)


async def safe_bot_operation(operation_name: str, operation_func):
    """Safely execute bot operations with retry logic."""
    try:
        await retry_with_backoff(operation_func)
        logger.info(f"Successfully completed: {operation_name}")
    except Exception as e:
        logger.error(f"Failed to {operation_name}: {e}")
        # Don't raise the exception to prevent app startup failure
        # The bot will retry on next operation


@app.on_event("startup")
async def on_startup():
    # await register_webhook() # TODO: add webhook

    # temp for dev - with retry logic
    await safe_bot_operation(
        "delete webhook", lambda: bot.delete_webhook(drop_pending_updates=False)
    )

    await safe_bot_operation("discard old updates", lambda: discard_old_updates(bot))

    # Start polling in background
    asyncio.create_task(dp.start_polling(bot))


@app.get("/ping")
async def ping():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="127.0.0.1", port=8000, reload=True, log_level="debug"
    )
