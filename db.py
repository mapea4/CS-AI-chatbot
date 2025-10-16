
"""Lightweight SQLAlchemy engine factory. Uses DATABASE_URL if provided."""
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from typing import Optional
from config import DATABASE_URL

_engine: Optional[Engine] = None

def get_engine(optional: bool = False) -> Optional[Engine]:
    global _engine
    if _engine is not None:
        return _engine

    if not DATABASE_URL:
        if optional:
            return None
        raise RuntimeError("DATABASE_URL not set; put it in your .env or .env.sample")

    _engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
    return _engine
