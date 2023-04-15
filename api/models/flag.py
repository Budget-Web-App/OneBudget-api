"""
License Goes Here
"""

from typing import Optional

from pydantic import BaseModel #pylint: disable=no-name-in-module


class BaseFlag(BaseModel):
    """
    Base Flag
    =========
    Data type used as request body for create flag request
    """

    display_name: str

    class Config:
        orm_mode = True


class IntermediaryFlag(BaseFlag):
    """
    Intermediary Flag
    =================
    
    """

    budget_id: str
    user_id: str

    class Config: # pylint: disable=missing-class-docstring
        orm_mode = True


class Flag(IntermediaryFlag):
    """
    Flag
    ====
    """
    
    id: Optional[str] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True
