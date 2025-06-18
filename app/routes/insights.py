from fastapi import (
    APIRouter,
    Depends,
    Query,
)


from app.models import UserModel

from app.schemas.insights_schema import InsightMonthly,CategoryInsightMonthly
from typing import Annotated, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.security import get_current_user
from app.services.insigths_services import get_income_for_month,get_expenses_by_category

router = APIRouter(prefix="/insights", tags=["Insigths"])

T_asyncsession = Annotated[AsyncSession, Depends(get_db)]
T_current_user = Annotated[UserModel, Depends(get_current_user)]
T_query = Annotated[
    Optional[str], Query(min_length=None, description="Procure por categorias")
]

@router.get("/monthly", response_model=InsightMonthly)
async def insigths_monthly(
    session: T_asyncsession,
    current_user: T_current_user,
    month: int = Query(ge=1, le=12, description="enter the month"),
    year: int = Query(ge=2000, description="enter the year"),
    skip: int = 0,
    limit: int = 10,
):
    """
    Get monthly insights including total income, expenses, and balance for a specific month and year.
    """

    return await get_income_for_month(session, current_user, month, year, skip, limit)


@router.get("/expenses_by_category", response_model=CategoryInsightMonthly)
async def insigths_expenses_by_category(
    session: T_asyncsession,
    current_user: T_current_user,
    query: T_query = None,
    skip: int = 0,
    limit: int = 10,
):
    """
    Get monthly expenses grouped by category.
    """

    return await get_expenses_by_category(session, current_user,query,skip,limit)
    