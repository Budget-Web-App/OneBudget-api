from fastapi import APIRouter

categories_router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@categories_router.get("/")
async def list_budgets():
    print("categories")