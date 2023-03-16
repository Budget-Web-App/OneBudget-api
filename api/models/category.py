from typing import List, Union, Optional

from pydantic import BaseModel

class BaseCategory(BaseModel):
    display_name: str
    
    class Config:
        orm_mode = True
        
class IntermediaryCategory(BaseCategory):
    budget_id: str
    user_id: str
    
    class Config:
        orm_mode = True
    

class Category(IntermediaryCategory):
    
    id: str
    
    class Config:
        orm_mode = True
    