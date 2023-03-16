from typing import List, Union, Optional

from pydantic import BaseModel
from datetime import date

class BaseBudget(BaseModel):
    display_name: str
    notes: Optional[str] = None
    
    class Config:
        orm_mode = True

class Budget(BaseBudget):
    id: Optional[str] = None
    accessed_date: date
    user_id: str
    
    class Config:
        orm_mode = True