import datetime

import pytest
from aiogram.types import Chat, Message, User

from app.handlers.translate import translate


@pytest.mark.asyncio
async def test_translate_handler(monkeypatch):
    captured = {}

    async def fake_answer(self, text, **kwargs):
        captured["text"] = text

    # Патчим метод answer у Message
    monkeypatch.setattr(Message, "answer", fake_answer, raising=False)

    msg = Message(
        message_id=1,
        date=datetime.datetime.now(),
        chat=Chat(id=123, type="private"),
        text="hello",
        from_user=User(
            id=123,
            is_bot=False,
            first_name="John",
            last_name="Doe",
            username="john_doe",
            language_code="en",
        ),
    )

    await translate(msg)
    assert captured["text"].find("Could not detect the language") != -1
    assert captured["text"].find("English") != -1
