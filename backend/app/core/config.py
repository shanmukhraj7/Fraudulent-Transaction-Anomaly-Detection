import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_ENV:      str = os.getenv("APP_ENV", "development")
    LOG_LEVEL:    str = os.getenv("LOG_LEVEL", "INFO")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:Shanmukh1430@db.bfcqpvzrycxkrgoyvmjm.supabase.co:5432/postgres",
    )
    MODEL_PATH: str = os.getenv("MODEL_PATH", "ML/models/isolation_forest.pkl")

settings = Settings()