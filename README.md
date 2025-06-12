# 🧠 Telegram Translator Bot

A universal translator bot built with **FastAPI**, **aiogram**, and **transformers**. The bot detects the input language, identifies the target language from the user prompt, and returns the translated message.

## 🚀 Features

- Built with **FastAPI** and **aiogram** for async performance
- Automatic language detection with `langdetect`
- Translation using lightweight HuggingFace transformer models
- Telegram Webhook support
- Dockerized development environment
- Ready for deployment with CI/CD

## 🔧 Requirements

- Python 3.11
- Telegram Bot Token from [@BotFather](https://t.me/botfather)

## 💠 Setup

```bash
git clone https://github.com/yourusername/fastapi-aiogram-translator.git
cd fastapi-aiogram-translator
poetry install
cp .env.example .env  # Fill in your BOT_TOKEN and WEBHOOK_URL
poetry run uvicorn app.main:app --reload
```

## 🐳 Run with Docker

```bash
docker-compose up --build
```

## 🌐 Webhook Endpoint

Webhook is exposed at:

```
POST /webhook
```

Make sure your `WEBHOOK_URL` in `.env` is publicly accessible (use [ngrok](https://ngrok.com) for local testing).

## 📁 Project Structure

```
app/
├── main.py            # FastAPI entrypoint
├── bot.py             # aiogram Bot & Dispatcher
├── api/routes.py      # Webhook route
├── core/config.py     # Environment config
├── core/webhook.py    # Webhook registration
├── ml/                # ML utilities: language detection, translation
tests/                 # Pytest test cases
```

## 📆 Tech Stack

- FastAPI
- aiogram
- transformers
- langdetect
- PostgreSQL (future use)
- Docker
- Poetry

## 📜 License

MIT
