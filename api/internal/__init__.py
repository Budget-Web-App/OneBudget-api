"""
License Goes Here
"""

from typing import Generator

from sqlalchemy.orm import Session

from api.db import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Gets Database Session

    Yields:
        Generator[Session, None, None]: Database session
    """
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()