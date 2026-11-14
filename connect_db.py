import psycopg2
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: int = 5432

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

conn = psycopg2.connect(
    dbname=settings.db_name,
    user=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port
)
cur = conn.cursor()
cur.execute("SELECT 1")
print(cur.fetchone())
cur.close()
conn.close()