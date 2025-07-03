import time

from aiogram import Bot

from app.bot import dp

TIME_LIMIT_MINUTES = 10 * 60


async def discard_old_updates(bot: Bot):
    """
    Read queue of updates and discard old ones.
    """
    now = time.time()
    updates = await bot.get_updates(offset=0, timeout=0)

    for update in updates:
        dt = (
            getattr(update, "date", None)
            or getattr(update.edited_message, "date", None)
            or getattr(update.callback_query, "message", None)
            or getattr(update.event, "date", None)
        )

        if dt and getattr(update.callback_query, "message", None):
            dt = getattr(update.callback_query, "message", None).date

        if dt and now - dt.timestamp() <= TIME_LIMIT_MINUTES * 60:
            await dp.feed_update(bot, update)

    if updates:
        await bot.get_updates(offset=updates[-1].update_id + 1, timeout=0)
