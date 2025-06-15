from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated

from app.database import get_db
from app.security import get_current_user
from app.models import UserModel
from app.schemas.expenses_schemas import ExpenseCreate, ExpensePublic,ExpenseList
from app.crud.expenses_crud import list_expenses
from app.services.expenses_sevices import (
        create_expense_and_update_income,
        update_expense_and_update_income,
        delete_expense_and_update_income
        )

router = APIRouter(prefix='/expenses', tags=["expenses"])

T_asyncsession   = Annotated[AsyncSession, Depends(get_db)]
T_current_user   = Annotated[UserModel,    Depends(get_current_user)]


@router.post('/', response_model=ExpensePublic, status_code=HTTPStatus.CREATED)
async def exp_create(
    session: T_asyncsession,
    current_user: T_current_user,
    expense: ExpenseCreate
    ):
        return await create_expense_and_update_income(session,current_user,expense)


@router.get('/',response_model=ExpenseList)
async def exp_list(
        session: T_asyncsession,
        current_user:T_current_user,
        skip: int = 0,
        limit: int = 100
        ):

            return await list_expenses(session,current_user,skip,limit)


@router.patch('/{expense_id}',response_model=ExpensePublic)
async def exp_update(
        expense_id:int,
        session:T_asyncsession,
        current_user:T_current_user,
        expense_data:ExpenseCreate
        ):
            return await update_expense_and_update_income(
                    session,
                    current_user,
                    expense_id,
                    expense_data
                    )


@router.delete('/{expense_id}')
async def exp_delete(
        expense_id:int,
        session:T_asyncsession,
        current_user:T_current_user,
        ):
            return await delete_expense_and_update_income(
                    session,
                    current_user,
                    expense_id
                    )




