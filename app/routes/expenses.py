from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated, Optional
from app.database import get_db
from app.security import get_current_user
from app.models import ExpensesModel, CategoryModel, UserModel
from app.schemas.expenses_schemas import ExpenseCreate, ExpensePublic
from app.services.ai_classifier import classify_expense  # nosso serviço de IA

router = APIRouter(prefix="/expenses", tags=["expenses"])

T_asyncsession   = Annotated[AsyncSession, Depends(get_db)]
T_current_user   = Annotated[UserModel,    Depends(get_current_user)]


@router.post("/", response_model=ExpensePublic, status_code=HTTPStatus.CREATED)
async def create_expense(
    session: T_asyncsession,
    current_user: T_current_user,
    expense: ExpenseCreate
):

    if not expense.category_id:
        suggested = await classify_expense(expense.description)

        stmt = select(CategoryModel.id).where(
            CategoryModel.user_id == current_user.id,
            CategoryModel.name.ilike(suggested)
        )
        result = await session.scalar(stmt)
        if result:
            expense.category_id = result
        else:
            stmt2 = select(CategoryModel.id).where(
                CategoryModel.user_id == current_user.id,
                CategoryModel.name == "Outros"
            )
            expense.category_id = await session.scalar(stmt2)


    db_expense = ExpensesModel(
        user_id     = current_user.id,
        category_id = expense.category_id,
        title       = expense.title,
        description = expense.description,
        amount      = expense.amount,
        date        = expense.date,
        status      = expense.status,
    )
    session.add(db_expense)
    await session.commit()
    await session.refresh(db_expense)

    return db_expense
