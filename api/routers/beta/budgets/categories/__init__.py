"""
License Goes Here
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from api.db.category import CategoryDb

from api.models.category import Category, BaseCategory, IntermediaryCategory
from api.models import Token
from api.internal import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

budgets_categories_router = APIRouter(
    prefix="/{budget_id}/categories",
    tags=["budget categories"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@budgets_categories_router.get("/")
async def list_budget_categories(
    budget_id: str,
    token: str = Depends(oauth2_scheme),
    db_session: Session = Depends(get_db)
) -> List[Category]:
    """
    Lists categories for the specific budget
    """

    token_data = Token.parse_token(token)

    return CategoryDb.list_categories(db_session, budget_id)


@budgets_categories_router.post("/")
async def create_budget_category(
    category: BaseCategory,
    budget_id: str,
    token: str = Depends(oauth2_scheme),
    db_session: Session = Depends(get_db)
) -> Category:
    """
    Creates a budget category
    """

    token_data = Token.parse_token(token)

    intermediary_category = IntermediaryCategory(
        display_name=category.display_name,
        budget_id=budget_id,
        user_id=token_data.user_id
    )

    return CategoryDb.add_category(db_session, intermediary_category)

@budgets_categories_router.get("/{category_id}")
async def get_budget_category(
    category_id: str,
    budget_id: str,
    token: str = Depends(oauth2_scheme),
    db_session: Session = Depends(get_db)) -> Optional[Category]:
    """
    Gets budget category with specified id
    """

    token_data = Token.parse_token(token)

    category = CategoryDb.get_category(db_session, category_id)

    if category is None:
        return None

    if category.budget_id != budget_id:
        raise HTTPException(
            status_code=403, detail="Budget id does not match current budget id")

    if category.user_id != token_data.user_id:
        raise HTTPException(
            status_code=403, detail="Category user id does not match current user id")

    return category
