from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from datetime import datetime

from sqlalchemy.orm import Session

from api.db.budget import BudgetDb

from api.models.budget import Budget, BaseBudget
from api.models import Token
from api.internal import get_db

from .categories import budgets_categories_router
from .flags import budget_flags_router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_budget_scopes(request: Request, security_scopes: SecurityScopes = SecurityScopes()):
    
    #token = request.headers["authorization"].replace("Bearer ", "")
    
    #token_data = Token.parse_token(token)
    
    budget_id = request.path_params.get("budget_id")
    
    security_scopes.scopes.append(f"{budget_id}.read")
    
    print(security_scopes.scopes)
    

budgets_router = APIRouter(
    prefix="/budgets",
    tags=["budgets"],
    #dependencies=[Security(get_budget_scopes)],
    responses={404: {"description": "Not found"}},
)

budgets_router.include_router(budgets_categories_router)
budgets_router.include_router(budget_flags_router)


@budgets_router.get("/")
async def list_budgets(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> List[Budget]:

    token_data = Token.parse_token(token)

    budgets = BudgetDb.list_budgets(db, token_data.user_id)

    return budgets

@budgets_router.post("/")
async def create_budget(budget: BaseBudget, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Budget:

    token_data = Token.parse_token(token)

    new_budget = Budget(display_name=budget.display_name, notes=budget.notes, user_id=token_data.user_id, accessed_date=datetime.today())

    budget = BudgetDb.add_budget(db, new_budget)

    return budget

@budgets_router.get("/{budget_id}")
async def get_budget(request: Request, budget_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[Budget]:

    token_data = Token.parse_token(token)

    budget = BudgetDb.get_budget(db, budget_id)

    if budget is None:
        return None
    
    if budget.user_id != token_data.user_id:
        raise HTTPException(status_code=403, detail="Budget user id does not match current user id")

    return budget
