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
    accessed_date: date
    user_id: str

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True
