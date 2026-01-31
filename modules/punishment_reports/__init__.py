import asyncio

from .listener import register_punishment_listener
from .commands import register_punishment_commands
from .scheduler import report_scheduler
from .storage import init_db


def setup_punishment_reports(dp, bot):
    # инициализация БД модуля
    init_db()

    # регистрация listener и команд
    register_punishment_listener(dp)
    register_punishment_commands(dp)

    # запуск планировщика
    asyncio.create_task(report_scheduler(bot))