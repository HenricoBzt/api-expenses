from fastapi import (
    APIRouter, 
    Depends, 
    Query,
    )

from decimal import Decimal
from app.models import (
    CategoryModel,
    ExpensesModel,
    MonthlyIncomeModel,
    UserModel)

from app.schemas.insights_schema import InsightMonthly
from typing import Annotated, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.security import get_current_user
from app.crud.insigths_services import get_income_for_month
router = APIRouter(
    prefix='/insights',
    tags=['Insigths']
    )

T_asyncsession = Annotated[AsyncSession, Depends(get_db)]
T_current_user = Annotated[UserModel, Depends(get_current_user)]

@router.get('/monthly',response_model=InsightMonthly)
async def insigths_monthly_endpoint(
    session: T_asyncsession,
    current_user: T_current_user,
    month: int = Query(ge=1,le=12,description='enter the month'),
    year: int = Query(ge=2000,description='enter the year'),
    skip: int = 0,
    limit: int = 10
    ):

    income = get_income_for_month(session=session,user_id=current_user.id,month=month,year=year)

    if income is None:
        income = Decimal(0)

    



    

    