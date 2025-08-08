from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Default to SQLite for local development to avoid requiring Postgres drivers
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ta_ai.db")

# SQLAlchemy engine and session
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)
Base = declarative_base()