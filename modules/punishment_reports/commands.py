from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import types
from aiogram.dispatcher import Dispatcher

from modules.punishment_reports.report import send_daily_reports

MOSCOW_TZ = ZoneInfo("Europe/Moscow")


async def report_today_command(message: types.Message):
    today = datetime.now(MOSCOW_TZ).date().isoformat()
    await send_daily_reports(message.bot, today)


def register_punishment_commands(dp: Dispatcher):
    dp.register_message_handler(
        report_today_command,
        commands=["report_today"],
        is_chat_admin=True  # чтобы не спамили все подряд
    )