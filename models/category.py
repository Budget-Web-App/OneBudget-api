"""
License Goes Here
"""

from pydantic import BaseModel #pylint: disable=no-name-in-module


class BaseCategory(BaseModel):
    """
    Base Category
    =============
    """

    display_name: str

    class Config: # pylint: disable=missing-class-docstring
        orm_mode = True


class IntermediaryCategory(BaseCategory):
    """
    Intermediary Category
    ====================
    
    """

    budget_id: str
    user_id: str

    class Config: # pylint: disable=missing-class-docstring
        orm_mode = True


class Category(IntermediaryCategory):
    """
    Category
    ========
    
    """

    id: str

    class Config: # pylint: disable=missing-class-docstring
        orm_mode = True
