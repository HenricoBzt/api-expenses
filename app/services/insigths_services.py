from http import HTTPStatus
from fastapi import HTTPException,Query
from typing import Optional,Annotated


from app.models import (
    CategoryModel,
    ExpensesModel,
    MonthlyIncomeModel,
    UserModel,
    StatusType,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract, func



async def get_income_for_month(
    session: AsyncSession,
    current_user: UserModel,
    month: int,
    year: int,
    skip: 0,
    limit: 100,
):
    try:
        income_in_month_or_year = (
            select(MonthlyIncomeModel.net_balance)
            .where(
                extract("month", MonthlyIncomeModel.initial_date) == month,
                extract("year", MonthlyIncomeModel.initial_date) == year,
                MonthlyIncomeModel.user_id == current_user.id,
            )
            .offset(skip)
            .limit(limit)
        )

        result_income = await session.scalar(income_in_month_or_year)

        if not result_income:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Insigth for monthly income not found",
            )

        total_expenses_stmt = select(
            func.coalesce(func.sum(ExpensesModel.amount), 0)
        ).where(
            extract("month", ExpensesModel.date) == month,
            extract("year", ExpensesModel.date) == year,
            ExpensesModel.user_id == current_user.id,
            ExpensesModel.status == StatusType.PAGO,
        )

        total_spent = await session.scalar(total_expenses_stmt)

        pending_expense_stmt = select(
            func.coalesce(func.sum(ExpensesModel.amount), 0)
        ).where(
            extract("month", ExpensesModel.date) == month,
            extract("year", ExpensesModel.date) == year,
            ExpensesModel.user_id == current_user.id,
            ExpensesModel.status.in_([StatusType.PENDENTE, StatusType.ATRASADO]),
        )

        total_pending_expense = await session.scalar(pending_expense_stmt)

        remaining_balance = result_income - total_pending_expense
        percentual_spent = (
            (total_spent / result_income) * 100 if result_income > 0 else 0
        )

        return {
            "current_income": result_income,
            "total_spent": total_spent,
            "remaining_balance": remaining_balance,
            "percentual_spent": percentual_spent,
            "year": year,
            "month": month,
        }

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching insights: {str(e)}",
        )


async def get_expenses_by_category(
    session: AsyncSession,
    current_user: UserModel,
    query: str = None,
    skip: int = 0,
    limit: int = 100,
):
    stmt_base = select(CategoryModel).where(
        CategoryModel.user_id == current_user.id,
    )

    result_category_stmt = stmt_base

    if query:
        result_category_stmt = stmt_base.where(CategoryModel.name.ilike(f"%{query}%"))

    result_category_stmt = result_category_stmt.offset(skip).limit(limit)
    result = await session.scalars(result_category_stmt)
    categories_list = result.all()

    if not categories_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Category not found."
        )

    expenses_by_category = []

    for category in categories_list:
        total_expenses_stmt = select(
            func.coalesce(func.sum(ExpensesModel.amount), 0)
        ).where(
            ExpensesModel.category_id == category.id,
            ExpensesModel.user_id == current_user.id,
            ExpensesModel.status == StatusType.PAGO,
        )

        total_expenses = await session.scalar(total_expenses_stmt)
        expenses_by_category.append(
            {
                "category_id": category.id,
                "category_name": category.name,
                "total_expenses": total_expenses,
            }
        )
    return {"expenses_by_category": expenses_by_category}
