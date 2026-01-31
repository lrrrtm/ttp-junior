from aiogram import types
from aiogram.dispatcher import Dispatcher

from config import (
    PUNISHMENT_REPORTS_ENABLED,
    PUNISHMENT_CHAT_ID,
    PUNISHMENT_SOURCE_TOPIC_ID,
)

from modules.punishment_reports.parser import parse_punishment_message
from modules.punishment_reports.storage import save_punishment


# usernames ботов, которые присылают наказания
ALLOWED_SOURCES = {
    "ttpchatbot",
}


async def punishment_listener(message: types.Message):
    # --- Фильтры безопасности ---
    if not message.is_topic_message:
        return

    if message.chat.id != PUNISHMENT_CHAT_ID:
        return

    if message.message_thread_id != PUNISHMENT_SOURCE_TOPIC_ID:
        return

    if not message.from_user or not message.from_user.username:
        return

    if message.from_user.username not in ALLOWED_SOURCES:
        return

    if not message.text:
        return

    # --- Парсинг ---
    parsed = parse_punishment_message(message.text)
    if not parsed:
        return

    # --- Сохранение ---
    save_punishment(
        action=parsed["action"],
        mode=parsed["mode"],
        moderator=parsed["moderator"],
    )


def register_punishment_listener(dp: Dispatcher):
    if not PUNISHMENT_REPORTS_ENABLED:
        return

    dp.register_message_handler(
        punishment_listener,
        content_types=types.ContentType.TEXT,
    )