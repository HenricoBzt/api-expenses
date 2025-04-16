from fastapi import APIRouter,Depends, HTTPException, Query
from http import HTTPStatus

from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from app.models import ExpensesModel,UserModel
from app.schemas.expenses_schemas import ExpenseCreate, ExpensePublic, ExpenseList, ExpenseUpdate
from typing import Annotated, Optional
from app.security import get_current_user

T_asyncsession = Annotated[AsyncSession, Depends(get_db)]
T_current_user = Annotated[UserModel, Depends(get_current_user)]
T_query = Annotated[Optional[str],Query(min_length=None,description='Procure por despesas')]

router = APIRouter(prefix='/expenses',tags=['expenses'])

@router.post('/', response_model=ExpensePublic)
async def create_expense(
        session: T_asyncsession,
        current_user: T_current_user,
        expense: ExpenseCreate):
        
        db_expense = ExpensesModel(
            user_id = current_user.id,
            category_id = expense.category_id,
            title = expense.title,
            description = expense.description,
            amount = expense.amount,
            date = expense.date,
            status = expense.status
        )

        session.add(db_expense)
        await session.commit()
        await session.refresh(db_expense) 
        return db_expense

@router.get('/search/', response_model=ExpenseList)
async def read_expenses(
        session:T_asyncsession,
        current_user: T_current_user,
        query: T_query = None,
        skip: int = 0,
        limit: int = 10
):
        stmt_base = select(ExpensesModel).order_by(ExpensesModel.title).where(ExpensesModel.user_id == current_user.id)
        stmt_query = stmt_base

        if query:
                stmt_query = stmt_base.where(ExpensesModel.title.ilike(f'%{query}%'))

        stmt_pagined = stmt_query.offset(skip).limit(limit)

        result =  await session.scalars(stmt_pagined)
        expenses_list = result.all()
        
        if not expenses_list:
                raise HTTPException(
                        status_code=HTTPStatus.NOT_FOUND,
                        detail ='Despesa não encontrada.'
                )

        return {'expenses': expenses_list}

@router.patch('/{expense_id}', response_model=ExpensePublic)
async def update_expense(
        session: T_asyncsession,
        expense_id: int,
        expense: ExpenseUpdate,
        current_user: T_current_user,
        ):

        expense_stmt = select(ExpensesModel).where(ExpensesModel.id == expense_id) 
        expense_obj = await session.scalar(expense_stmt)

        if not expense_obj:
                raise HTTPException(
                        status_code= HTTPStatus.NOT_FOUND,
                        detail='Despesa não encontrada'
                )

        for key, value in expense.model_dump(exclude_unset=True).items():
                setattr(expense_obj,key,value)

        
        await session.commit()
        await session.refresh(expense_stmt )
  
        return expense_stmt

@router.delete('/{id}')
async def delete_expense(
        session: T_asyncsession,
        current_user: T_current_user,
        expense_id: int,
        ):

        expense_stmt = select(ExpensesModel).where(ExpensesModel.id == expense_id)
        expense_obj = await session.scalar(expense_stmt)

        if not expense_obj:
                raise HTTPException(
                        status_code=HTTPStatus.NOT_FOUND,
                        detail='Despesa não encontrada'
                )


        if expense_obj.user_id != current_user.id:
                raise HTTPException(
                        status_code=HTTPStatus.FORBIDDEN,
                        detail= 'Not enough permission' 
                )
        
        await session.delete(expense_obj)
        await session.commit()
        return {'message': 'Expense deleted'}
                


        


