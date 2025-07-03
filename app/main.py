import asyncio

from fastapi import FastAPI

from app.api.routes import router
from app.bot import bot, dp
from app.core.webhook import register_webhook
from app.logging_conf import setup_logging
from app.services.message_filter import discard_old_updates

setup_logging()
app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def on_startup():
    # await register_webhook() # TODO: add webhook

    # temp for dev
    await bot.delete_webhook(drop_pending_updates=False)
    await discard_old_updates(bot)
    asyncio.create_task(dp.start_polling(bot))


@app.get("/ping")
async def ping():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="127.0.0.1", port=8000, reload=True, log_level="debug"
    )
