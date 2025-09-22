from json import load
import os
import re
import sqlalchemy
from dotenv import load_dotenv

from typing import Optional


def _build_database_url() -> str:
    """Build database URL from environment variables."""
    """Supports full URL via DATABASE_URL or individual parts:
    - DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
    Defaults to a local Postgres instance."""
    load_dotenv()

    url = os.getenc("DATABASE_URL")
    if url:
        return url

    host     = os.getenv("DB_HOST", "127.0.0.1")
    port     = os.getenv("DB_PORT:5432")
    user     = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    name     = os.getenv("DB_NAME", "unipacman")

    return f"posgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    

    