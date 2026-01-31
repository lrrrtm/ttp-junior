import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from aiogram import Bot

from config import PUNISHMENT_REPORTS_ENABLED
from modules.punishment_reports.report import send_daily_reports


# Часовой пояс Москвы
MOSCOW_TZ = ZoneInfo("Europe/Moscow")


async def report_scheduler(bot: Bot):
    """
    Фоновый планировщик.
    Каждый день в 00:00 по МСК отправляет отчёты за прошедший день.
    НЕ зависит от команды /report_today.
    """

    if not PUNISHMENT_REPORTS_ENABLED:
        return

    while True:
        now = datetime.now(MOSCOW_TZ)

        # Следующая полночь по МСК
        next_run = (now + timedelta(days=1)).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        # Спим до 00:00
        sleep_seconds = (next_run - now).total_seconds()
        await asyncio.sleep(sleep_seconds)

        # Отчёт за прошедший день
        report_date = (next_run - timedelta(days=1)).date().isoformat()

        await send_daily_reports(bot, report_date)