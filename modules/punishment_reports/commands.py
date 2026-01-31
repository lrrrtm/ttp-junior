from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import PUNISHMENT_REPORTS_ENABLED
from .report import send_daily_reports  # ← ОТНОСИТЕЛЬНЫЙ ИМПОРТ


MOSCOW_TZ = ZoneInfo("Europe/Moscow")

router = Router()


@router.message(Command("report_today"))
async def report_today_command(message: Message):
    if not PUNISHMENT_REPORTS_ENABLED:
        return

    # Ограничение: только админы
    if message.chat.type in ("group", "supergroup"):
        member = await message.bot.get_chat_member(
            message.chat.id,
            message.from_user.id
        )
        if member.status not in ("administrator", "creator"):
            return

    today = datetime.now(MOSCOW_TZ).date().isoformat()
    await send_daily_reports(message.bot, today)


def register_punishment_commands(dp):
    if not PUNISHMENT_REPORTS_ENABLED:
        return

    dp.include_router(router)