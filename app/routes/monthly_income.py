from fastapi import (
    APIRouter,
    Depends,
)

from http import HTTPStatus

from app.database import get_db

from app.schemas.monthlyincome_schema import (
    MonthlyIncomeCreate,
    MonthlyIncomePublic,
    MonthlyIncomeUpdate,
)
from app.models import UserModel
from app.security import get_current_user
from app.crud.monthlyincome_crud import (
    create_monthly_income_crud,
    get_monthly_income,
    update_monthlyincome,
    delete_monthlyincome,
)
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession


T_current_user = Annotated[UserModel, Depends(get_current_user)]
T_asyncsession = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter(
    prefix="/monthly_income",
    tags=["Monthly Income"],
)


@router.post("/", response_model=MonthlyIncomePublic, status_code=HTTPStatus.CREATED)
async def create_monthly_income(
    session: T_asyncsession,
    current_user: T_current_user,
    monthly_income_data: MonthlyIncomeCreate,
):

    return await create_monthly_income_crud(
        session,
        monthly_income_data,
        current_user,
    )


@router.get("/", response_model=MonthlyIncomePublic)
async def read_monthly_income(
    session: T_asyncsession,
    current_user: T_current_user,
):

    return await get_monthly_income(
        session,
        current_user
    )


@router.patch("/{monthly_income_id}", response_model=MonthlyIncomePublic)
async def update_monthly_income(
    session: T_asyncsession,
    current_user: T_current_user,
    monthly_income: MonthlyIncomeUpdate,
    monthly_income_id: int,
):
    return await update_monthlyincome(
        session,
        current_user,
        monthly_income_id,
        monthly_income,
    )


@router.delete("/{monthly_income_id}")
async def delete_monthly_income(
    session: T_asyncsession,
    current_user: T_current_user,
    monthly_income_id: int,
):
    return await delete_monthlyincome(
        session,
        current_user,
        monthly_income_id,
    )
