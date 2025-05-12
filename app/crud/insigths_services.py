
from http import HTTPStatus
from app.models import (
    CategoryModel,
    ExpensesModel,
    MonthlyIncomeModel,
    UserModel
    )
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,extract

async def get_income_for_month(
    session:AsyncSession,
    user_id:int,
    month: int, 
    year: int ,
    ):
    
    income_in_month_or_year = select(MonthlyIncomeModel.net_balance).where(
        extract('month', MonthlyIncomeModel.initial_date) == month,
        extract('year', MonthlyIncomeModel.initial_date) == year,
        MonthlyIncomeModel.user_id == user_id
    )

    result_income = await session.scalar(income_in_month_or_year)
    
    return result_income


