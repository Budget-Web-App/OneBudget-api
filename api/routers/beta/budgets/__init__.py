"""
License Goes Here
"""

from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from fastapi_pagination import Page, paginate

from sqlalchemy.orm import Session

from api.db.budget import BudgetDb

from api.models.budget import Budget, BaseBudget
from api.models import Token
from api.internal import get_db

from api.routers.beta.budgets.categories import budgets_categories_router
from api.routers.beta.budgets.flags import budget_flags_router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

budgets_router = APIRouter(
    prefix="/budgets",
    tags=["budgets"],
    responses={404: {"description": "Not found"}},
)

budgets_router.include_router(budgets_categories_router)
budgets_router.include_router(budget_flags_router)


@budgets_router.get(path="/", response_model=Page[Budget])
async def list_budgets(
    token: str = Depends(oauth2_scheme),
    db_session: Session = Depends(get_db)
) -> Page[Budget]:
    """
    Lists all budgets for the current user
    """

    token_data = Token.parse_token(token)

    budgets = BudgetDb.list_budgets(db_session, token_data.user_id)

    return paginate(budgets)


@budgets_router.post("/")
async def create_budget(
    budget: BaseBudget,
    token: str = Depends(oauth2_scheme),
    db_session: Session = Depends(get_db)
) -> Budget:
    """
    Creates a new budget
    """

    token_data = Token.parse_token(token)

    new_budget = Budget(
        display_name=budget.display_name,
        notes=budget.notes,
        user_id=token_data.user_id,
        accessed_date=datetime.today()
    )

    return BudgetDb.add_budget(db_session, new_budget)


@budgets_router.get("/{budget_id}")
async def get_budget(
    budget_id: str,
    token: str = Depends(oauth2_scheme),
    db_session: Session = Depends(get_db)
) -> Optional[Budget]:
    """
    Gets budget by id
    """

    token_data = Token.parse_token(token)

    budget = BudgetDb.get_budget(db_session, budget_id)

    if budget is None:
        return None

    if budget.user_id != token_data.user_id:
        raise HTTPException(
            status_code=403,
            detail="Budget user id does not match current user id"
        )

    return budget
