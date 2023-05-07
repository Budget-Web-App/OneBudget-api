"""
License Goes Here
"""

from fastapi import APIRouter

from .budgets import budgets_router
from .oauth import oauth_router

beta_router = APIRouter(
    prefix="/beta",
    tags=["beta"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

beta_router.include_router(budgets_router)
beta_router.include_router(oauth_router)
