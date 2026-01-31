import asyncio

from modules.punishment_reports.listener import register_punishment_listener
from modules.punishment_reports.storage import init_db
from modules.punishment_reports.scheduler import report_scheduler
from modules.punishment_reports.commands import register_punishment_commands


def setup_punishment_reports(dp, bot):
    # Инициализация БД
    init_db()

    # Регистрация listener'а и команд
    register_punishment_listener(dp)
    register_punishment_commands(dp)

    # Запуск фонового scheduler'а
    asyncio.create_task(report_scheduler(bot))