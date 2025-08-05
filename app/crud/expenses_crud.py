from fastapi import HTTPException
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from app.models import ExpensesModel, UserModel


from app.schemas.expenses_schemas import ExpenseCreate


# Function for create expenses.


async def create_expense(
    session: AsyncSession, current_user: UserModel, expense_create: ExpenseCreate
):

    new_expense = ExpensesModel(
        user_id=current_user.id,
        category_id=expense_create.category_id,
        title=expense_create.title,
        description=expense_create.description,
        amount=expense_create.amount,
        date=expense_create.date,
        status=expense_create.status,
    )

    session.add(new_expense)
    await session.commit()
    await session.refresh(new_expense)
    return new_expense


# Function for list expenses.
async def list_expenses(
    session: AsyncSession,
    current_user: UserModel,
    skip: int,
    limit: int,
):

    stmt = (
        select(ExpensesModel)
        .where(ExpensesModel.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )

    obj_expense = await session.scalars(stmt)
    expenses_list = obj_expense.all()

    if not expenses_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="expense not found."
        )

    return {"expenses": expenses_list}


# Function for get expense by id.
async def get_expense_by_id(
    session: AsyncSession,
    current_user: UserModel,
    expense_id: int,
):
    stmt = select(ExpensesModel).where(
        ExpensesModel.user_id == current_user.id, ExpensesModel.id == expense_id
    )

    obj_expense = await session.scalar(stmt)

    if not obj_expense:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="expense not found."
        )

    if current_user.id != obj_expense.user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="not enough permission for update this expense.",
        )

    return obj_expense


# Function Update Expenses
async def update_expenses(
    session: AsyncSession,
    current_user: UserModel,
    expense_id: int,
    expense_data: ExpenseCreate,
):

    stmt = select(ExpensesModel).where(
        ExpensesModel.user_id == current_user.id, ExpensesModel.id == expense_id
    )

    obj_expense = await session.scalar(stmt)

    if current_user.id != obj_expense.user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="not enough permission for update this expense.",
        )

    for key, value in expense_data.model_dump(exclude_unset=True).items():
        setattr(obj_expense, key, value)

    await session.commit()
    await session.refresh(obj_expense)

    return obj_expense


# Function Delete Expenses
async def delete_expense(
    session: AsyncSession, current_user: UserModel, expense_id: int
):
    stmt = select(ExpensesModel).where(
        ExpensesModel.user_id == current_user.id, ExpensesModel.id == expense_id
    )

    obj_expense = await session.scalar(stmt)

    if current_user.id != obj_expense.user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="not enough permission for update this expense.",
        )

    if not obj_expense:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="expense not found."
        )

    await session.delete(obj_expense)
    await session.commit()

    return {"message": "Expense deleted."}
