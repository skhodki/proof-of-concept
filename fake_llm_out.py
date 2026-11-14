"""
fake_llm_out.py

A placeholder for the output side of the LLM. It takes the original question
and the rows returned by the database, and produces a natural-language answer.
For now, the sentences are built from a template; later, this module will call
a real LLM and the rest of the system will not need to change.
"""

import asyncio
from datetime import datetime


def _relative_date(start: datetime, now: datetime) -> str:
    """Return a human phrase for the date, computed deterministically."""
    days = (start.date() - now.date()).days
    if days == 0:
        return "today"
    if days == 1:
        return "tomorrow"
    if days == 2:
        return "the day after tomorrow"
    if 0 < days < 7:
        return f"this coming {start.strftime('%A')}"
    return start.strftime("%A, %B %d")


def _format_time(start: datetime) -> str:
    """Return a 12-hour time like '7 p.m.' from a 24-hour timestamp."""
    hour = start.hour % 12 or 12
    suffix = "a.m." if start.hour < 12 else "p.m."
    if start.minute:
        return f"{hour}:{start.minute:02d} {suffix}"
    return f"{hour} {suffix}"


async def rows_to_answer(question: str, rows: list[dict]) -> str:
    """
    Convert a question and its result rows into a natural-language answer.

    This is async so that the real LLM call can replace the body without
    changing the caller. The current implementation is a deterministic
    template.
    """
    await asyncio.sleep(0)  # simulate the await of a real network call

    if not rows:
        return "I could not find any meetings matching that request."

    now = datetime.now()
    sentences = []
    for row in rows:
        start = datetime.fromisoformat(row["start_time"])
        sentences.append(
            f'The meeting "{row["title"]}" will take place at '
            f'{row["location"]} {_relative_date(start, now)} '
            f'at {_format_time(start)}'
        )

    if len(sentences) == 1:
        return sentences[0]
    return "Here are the meetings I found:\n\n" + "\n".join(
        f"- {s}" for s in sentences
    )