from typing import List, Union, Optional

from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    id: Optional[str] = None
    email: str
    pass_hash: bytes
    timezone: Optional[str] = None
    registered_date: Optional[date] = None
    
    class Config:
        orm_mode = True