from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from datetime import datetime

from sqlalchemy.orm import Session

from api.db.flag import FlagDb

from api.models.flag import Flag, IntermediaryFlag, BaseFlag
from api.models import Token
from api.internal import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

budget_flags_router = APIRouter(
    prefix="/{budget_id}/flags",
    tags=["budget flags"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)

@budget_flags_router.get("/")
async def list_budget_flags(budget_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> List[Flag]:
    
    return FlagDb.list_flags(db, budget_id)

@budget_flags_router.post("/")
async def create_budget_flag(flag: BaseFlag, budget_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Flag:
    
    token_data = Token.parse_token(token)
    
    intermediary_flag = IntermediaryFlag(
        display_name=flag.display_name,
        budget_id=budget_id,
        user_id=token_data.user_id
    )
    
    return FlagDb.add_flag(db, intermediary_flag)

@budget_flags_router.get("/{flag_id}")
async def get_budget_flag(budget_id: str, flag_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Flag:
    
    token_data = Token.parse_token(token)
    
    flag = FlagDb.get_flag(db, flag_id)
    
    if flag is None:
        return None
    
    if flag.budget_id != budget_id:
        raise HTTPException(status_code=403, detail="Budget id does not match current budget id")
    
    if flag.user_id != token_data.user_id:
        raise HTTPException(status_code=403, detail="Flag user id does not match current user id")
    
    return flag