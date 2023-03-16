from fastapi import APIRouter

months_router = APIRouter(
    prefix="/months",
    tags=["months"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@months_router.get("/")
async def list_budgets():
    print("months")