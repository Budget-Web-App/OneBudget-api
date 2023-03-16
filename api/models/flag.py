from typing import Optional

from pydantic import BaseModel

class BaseFlag(BaseModel):
    
    display_name: str
    
    class Config:
        orm_mode = True
    
class IntermediaryFlag(BaseFlag):
    
    budget_id: str
    user_id: str
    
    class Config:
        orm_mode = True

class Flag(IntermediaryFlag):
    id: Optional[str] = None
    
    class Config:
        orm_mode = True