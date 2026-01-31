from aiogram import Router
from aiogram.types import Message

from config import (
    PUNISHMENT_REPORTS_ENABLED,
    PUNISHMENT_CHAT_ID,
    PUNISHMENT_SOURCE_TOPIC_ID,
)

from .storage import save_punishment
from .parser import parse_punishment_message


# usernames ботов, которые присылают наказания (БЕЗ @)
ALLOWED_SOURCES = {
    "ttpchatbot",
}

router = Router()


@router.message()
async def punishment_listener(message: Message):
    if not PUNISHMENT_REPORTS_ENABLED:
        return

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


def register_punishment_listener(dp):
    """
    Подключаем router к Dispatcher (aiogram 3)
    """
    if not PUNISHMENT_REPORTS_ENABLED:
        return

    dp.include_router(router)