"""
Supabase PostgreSQL & SQLite Database Configuration & Session Management
Supports cloud database connection via Supabase PostgreSQL or fallback to local SQLite.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "food_quality.db")

# Read database URL from environment (e.g., Supabase PostgreSQL connection string)
DATABASE_URL = os.getenv("DATABASE_URL", os.getenv("SUPABASE_DB_URL", f"sqlite:///{DB_PATH}"))

# Fix Heroku/Supabase postgres:// scheme if needed for SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
