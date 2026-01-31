import re
from typing import Optional, Dict


# Константы режимов
POLIT_1 = "polit_1"
POLIT_2 = "polit_2"

# Константы действий
ACTION_MUT = "mut"
ACTION_BAN = "ban"
ACTION_UNBAN = "unban"


def parse_punishment_message(text: str) -> Optional[Dict[str, str]]:
    """
    Парсит сообщение о наказании.
    Возвращает dict с action, mode, moderator или None.
    """

    text = text.strip()

    # --- Определяем действие ---
    if "МУТ" in text:
        action = ACTION_MUT
        moderator_match = re.search(r"Наказал:\s*(.+)", text)

    elif "БАН" in text and "РАЗБАН" not in text:
        action = ACTION_BAN
        moderator_match = re.search(r"Наказал:\s*(.+)", text)

    elif "РАЗБАН" in text:
        action = ACTION_UNBAN
        moderator_match = re.search(r"Исполнитель:\s*(.+)", text)

    else:
        return None  # не наше сообщение

    if not moderator_match:
        return None

    moderator = moderator_match.group(1).strip()

    # --- Определяем режим ---
    if "Режим: Полит 1" in text:
        mode = POLIT_1
    elif "Режим: Полит 2" in text:
        mode = POLIT_2
    else:
        return None

    return {
        "action": action,
        "mode": mode,
        "moderator": moderator,
    }