from typing import Dict

from aiogram import Bot

from config import PUNISHMENT_REPORT_TOPIC_ID
from modules.punishment_reports.storage import get_daily_summary


# Человекочитаемые названия режимов
MODE_TITLES = {
    "polit_1": "🛡 Режим: Polit 1",
    "polit_2": "🛡 Режим: Polit 2",
}


def build_daily_report(date: str, mode: str, summary: Dict) -> str:
    """
    Формирует текст дневного отчёта по одному режиму.
    """

    mut_count = summary.get("mut", 0)
    ban_count = summary.get("ban", 0)
    unban_count = summary.get("unban", 0)
    moderators = summary.get("moderators", {})

    # Если вообще ничего не было — отчёт не нужен
    if mut_count == 0 and ban_count == 0 and unban_count == 0:
        return ""

    lines = []

    lines.append(f"📊 Отчёт за {date}")
    lines.append(MODE_TITLES.get(mode, f"Режим: {mode}"))
    lines.append("")

    lines.append(f"🔇 Муты: {mut_count}")
    lines.append(f"⛔ Баны: {ban_count}")
    lines.append(f"✅ Разбаны: {unban_count}")
    lines.append("")

    if moderators:
        lines.append("👮 Модераторы:")

        # Сортируем по количеству действий
        sorted_mods = sorted(
            moderators.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Топ-3, остальные — в "прочие"
        top_mods = sorted_mods[:3]
        other_count = sum(count for _, count in sorted_mods[3:])

        for name, count in top_mods:
            lines.append(f"• {name} — {count}")

        if other_count > 0:
            lines.append(f"• прочие — {other_count}")

    return "\n".join(lines)


async def send_daily_reports(bot: Bot, target_date: str):
    """
    Отправляет отчёты по всем режимам за указанную дату.
    Используется и scheduler'ом, и командой /report_today.
    """

    for mode in ("polit_1", "polit_2"):
        summary = get_daily_summary(target_date, mode)
        text = build_daily_report(target_date, mode, summary)

        if not text:
            continue

        await bot.send_message(
            chat_id=PUNISHMENT_REPORT_TOPIC_ID,
            text=text
        )