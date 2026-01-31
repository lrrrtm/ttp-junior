import sqlite3
from datetime import date
from typing import Dict


DB_PATH = "database/punishment_reports.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS punishment_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            action TEXT NOT NULL,
            mode TEXT NOT NULL,
            moderator TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_punishment(action: str, mode: str, moderator: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO punishment_logs (date, action, mode, moderator)
        VALUES (?, ?, ?, ?)
        """,
        (
            date.today().isoformat(),
            action,
            mode,
            moderator,
        )
    )

    conn.commit()
    conn.close()


def get_daily_summary(target_date: str, mode: str) -> Dict:
    """
    Возвращает сводку за день и режим.
    Учитывает: mut, ban, unban
    """

    conn = get_connection()
    cursor = conn.cursor()

    # --- Счётчик действий ---
    cursor.execute(
        """
        SELECT action, COUNT(*)
        FROM punishment_logs
        WHERE date = ? AND mode = ?
        GROUP BY action
        """,
        (target_date, mode)
    )

    action_counts = {row[0]: row[1] for row in cursor.fetchall()}

    # --- Статистика по модераторам (все действия) ---
    cursor.execute(
        """
        SELECT moderator, COUNT(*)
        FROM punishment_logs
        WHERE date = ? AND mode = ?
        GROUP BY moderator
        ORDER BY COUNT(*) DESC
        """,
        (target_date, mode)
    )

    moderators = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()

    return {
        "mut": action_counts.get("mut", 0),
        "ban": action_counts.get("ban", 0),
        "unban": action_counts.get("unban", 0),
        "moderators": moderators,
    }