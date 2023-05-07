"""
License Goes Here
"""

from typing import Optional
from datetime import date

from pydantic import BaseModel # pylint: disable=no-name-in-module


class BaseBudget(BaseModel):
    """
    Base Budget
    ===========
    
    """

    display_name: str
    notes: Optional[str] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class Budget(BaseBudget):
    """
    Budget
    ======
    
    """

    id: Optional[str] = None
    display_name: Optional[str] = None
    accessed_date: Optional[date] = None
    user_id: Optional[str] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True
