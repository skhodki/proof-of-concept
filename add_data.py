import psycopg2
from config import settings

# --- Connect to database ---
conn = psycopg2.connect(
    dbname=settings.db_name,
    user=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port
)
cur = conn.cursor()

# --- Ensure that a "meetings" table exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS meetings (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        location TEXT NOT NULL,
        start_time TIMESTAMP NOT NULL
    )
""")
conn.commit()
print("Table 'meetings' is ready.")

# --- Ensure the table is empty before adding a row ---
cur.execute("TRUNCATE meetings RESTART IDENTITY;")
conn.commit()

# --- Insert multiple rows ---
cur.execute("""
    INSERT INTO meetings (title, location, start_time)
    VALUES
        (%s, %s, %s),
        (%s, %s, %s),
        (%s, %s, %s)
    RETURNING id
    """,
    (
        "Python for AI", "Maker Lab", "2026-11-20 19:00:00",
        "LLM and SQL", "City Library", "2026-11-21 18:30:00",
        "Database design", "Café Olé", "2026-11-22 17:00:00",
    )
)
new_ids = [row[0] for row in cur.fetchall()]
conn.commit()
print(f"Inserted meetings with ids={new_ids}.")

# --- Query all rows ---
cur.execute("SELECT id, title, location, start_time FROM meetings")
rows = cur.fetchall()
print("\nAll meetings:")
for row in rows:
    print(row)

# --- Clean up ---
cur.close()
conn.close()