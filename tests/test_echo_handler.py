import pytest, datetime
from aiogram.types import Message, Chat
from app.handlers.echo import echo

@pytest.mark.asyncio
async def test_echo_handler(monkeypatch):
    captured = {}

    async def fake_answer(self, text, **kwargs):
        captured["text"] = text

    # Патчим метод answer у Message
    monkeypatch.setattr(Message, "answer", fake_answer, raising=False)

    msg = Message(
        message_id=1,
        date=datetime.datetime.now(),
        chat=Chat(id=123, type="private"),
        text="hello"
    )

    await echo(msg)
    assert captured["text"] == "You said: hello"
