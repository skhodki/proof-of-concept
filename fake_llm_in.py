"""
fake_llm.py

A placeholder for the LLM. It takes a natural-language
question and returns an SQL query. For now, the mapping is
hard-coded; later, this module will call a real LLM and the
rest of the system will not need to change.
"""

import asyncio


# Hard-coded mapping from question to SQL.
# Add entries as the tutorial introduces new questions.
RESPONSES = {
    "find all meetings": "SELECT id, title, location, start_time FROM meetings",
    "find ai meetings": (
        "SELECT id, title, location, start_time FROM meetings "
        "WHERE title ILIKE '%AI%' OR title ILIKE '%LLM%'"
    ),
    "find meetings on friday": (
        "SELECT id, title, location, start_time FROM meetings "
        "WHERE EXTRACT(ISODOW FROM start_time) = 5"
    ),
}


async def question_to_sql(question: str) -> str:
    """
    Convert a natural-language question into a SQL query.

    This is async so that the rest of the system is already
    shaped for the real LLM call, which will be async. The
    current implementation is synchronous (a dictionary
    lookup) wrapped in asyncio.sleep(0) to make the async
    behaviour explicit.
    """
    await asyncio.sleep(0)  # simulate the await of a real network call

    key = question.strip().lower()
    if key in RESPONSES:
        return RESPONSES[key]

    # A predictable fallback, so the endpoint always returns something.
    return "SELECT id, title, location, start_time FROM meetings"