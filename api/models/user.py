"""
License Goes Here
"""

from typing import Optional
from datetime import date

from pydantic import BaseModel #pylint: disable=no-name-in-module

class User(BaseModel):
    """
    User
    ====
    User Data Type
    """

    id: Optional[str] = None
    email: str
    pass_hash: bytes
    timezone: Optional[str] = None
    registered_date: Optional[date] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True
