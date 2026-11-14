from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

import psycopg2
from pydantic import BaseModel
from config import settings

from fake_llm_in import question_to_sql
from fake_llm_out import rows_to_answer

app = FastAPI()

class AskRequest(BaseModel):
    question: str


@app.post("/ask")
async def ask(request: AskRequest):
    # 1. Translate the question into SQL (placeholder for now).
    sql = await question_to_sql(request.question)
    print(f"[ask] sql: {sql}")

    # 2. Execute the SQL. NOTE: SQL IS UNTRUSTWORTHY.
    conn = psycopg2.connect(
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port
    )

    try:
        cur = conn.cursor()
        cur.execute(sql)
        raw_rows = cur.fetchall()
        rows = [
            {"id": r[0], "title": r[1], "location": r[2],
             "start_time": r[3].isoformat()}
            for r in raw_rows
        ]
    finally:
        cur.close()
        conn.close()

    # 3. Convert the rows into a natural-language answer (placeholder for now).
    answer = await rows_to_answer(request.question, rows)
    print(f"[ask] answer: {answer}")

    return {
        "question": request.question,
        "sql": sql,
        "rows": rows,
        "answer": answer,
    }


app.mount("/", StaticFiles(directory=Path("public"), html=True))