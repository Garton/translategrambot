from fastapi import FastAPI
from app.api.routes import router
from app.core.webhook import register_webhook

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def on_startup():
    await register_webhook()

@app.get("/ping")
async def ping():
    return {"status": "ok"}
