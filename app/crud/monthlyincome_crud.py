from fastapi import HTTPException, Depends
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, extract
from typing import Annotated

from app.models import MonthlyIncomeModel, UserModel

from app.security import get_current_user
from app.schemas.monthlyincome_schema import (
    MonthlyIncomeCreate,
    MonthlyIncomeUpdate,
)

T_current_user = Annotated[UserModel, Depends(get_current_user)]


async def create_monthly_income_crud(
    session: AsyncSession,
    monthlyincome_data: MonthlyIncomeCreate,
    current_user: T_current_user,
):

    stmt = select(MonthlyIncomeModel).where(
        extract("month", MonthlyIncomeModel.initial_date)
        == monthlyincome_data.initial_date.month,
        extract("year", MonthlyIncomeModel.initial_date)
        == monthlyincome_data.initial_date.year,
        MonthlyIncomeModel.user_id == current_user.id,
    )

    existing_income = await session.scalar(stmt)

    if existing_income:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="There is already a registered monthly income please delete or update.",
        )

    monthly_income_db = MonthlyIncomeModel(
        **monthlyincome_data.model_dump(), user_id=current_user.id
    )

    session.add(monthly_income_db)
    await session.commit()
    await session.refresh(monthly_income_db)

    return monthly_income_db


async def get_monthly_income(
    session: AsyncSession,
    current_user: T_current_user,
):
    stmt = select(MonthlyIncomeModel).where(
        MonthlyIncomeModel.user_id == current_user.id
    )
    obj_monthlyincome = await session.scalar(stmt)

    if not obj_monthlyincome:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="monthly income not found."
        )

    return obj_monthlyincome


async def update_monthlyincome(
    session: AsyncSession,
    current_user: T_current_user,
    monthlyincome_id: int,
    monthlyincome_data: MonthlyIncomeUpdate,
):
    stmt = select(MonthlyIncomeModel).where(
        MonthlyIncomeModel.id == monthlyincome_id,
        MonthlyIncomeModel.user_id == current_user.id,
    )

    obj_monthlyincome = await session.scalar(stmt)

    if obj_monthlyincome is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="monthly income not found."
        )

    for key, value in monthlyincome_data.model_dump(exclude_unset=True).items():
        setattr(obj_monthlyincome, key, value)

    await session.commit()
    await session.refresh(obj_monthlyincome)

    return obj_monthlyincome


async def delete_monthlyincome(
    session: AsyncSession, current_user: T_current_user, monthlyincome_id: int
):
    stmt = select(MonthlyIncomeModel).where(
        MonthlyIncomeModel.id == monthlyincome_id,
        MonthlyIncomeModel.user_id == current_user.id,
    )

    obj_montlhyincome = await session.scalar(stmt)

    if not obj_montlhyincome:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="montlhyincome not found."
        )

    await session.delete(obj_montlhyincome)
    await session.commit()

    return {"mensage": "Monthly Income deleted."}
