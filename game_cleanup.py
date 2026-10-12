"""Auto-delete helpers for non-Mafia game messages."""
import asyncio
import logging

logger = logging.getLogger(__name__)

async def delete_message_after(context, chat_id, message_id, seconds=60):
    if seconds > 0:
        await asyncio.sleep(seconds)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as exc:
        logger.debug("Auto-delete skipped for %s/%s: %s", chat_id, message_id, exc)

async def hide_command(context, message):
    """Delete the user's game command shortly after its response is sent."""
    if message is None:
        return
    await asyncio.sleep(0.5)
    try:
        await context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
    except Exception as exc:
        logger.debug("Command auto-delete skipped: %s", exc)

def schedule_delete(context, message, seconds=60):
    if message is not None:
        context.application.create_task(
            delete_message_after(context, message.chat_id, message.message_id, seconds)
        )

async def reply_and_expire(message, context, *args, **kwargs):
    """Send a standalone message so deleting the command cannot break replies."""
    if message is None:
        return None
    # Pass chat_id positionally so the first positional argument (text)
    # cannot accidentally bind to chat_id as well.
    sent = await context.bot.send_message(
        message.chat_id,
        *args,
        **kwargs,
    )
    schedule_delete(context, sent, 60)
    return sent

async def photo_and_expire(message, context, *args, **kwargs):
    """Send a standalone photo, never replying to an auto-deleted command."""
    if message is None:
        return None
    sent = await context.bot.send_photo(
        message.chat_id,
        *args,
        **kwargs,
    )
    schedule_delete(context, sent, 60)
    return sent
