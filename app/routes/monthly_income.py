from fastapi import (
     APIRouter, 
     Depends, 
     HTTPException,
     )

from http import HTTPStatus

from app.database import get_db
from app.models import MonthlyIncomeModel
from app.schemas.monthlyincome_schema import (
    MonthlyIncomeCreate, 
    MonthlyIncomePublic, 
    MonthlyIncomeList, 
    MonthlyIncomeUpdate,
    )
from app.models import UserModel
from app.security import get_current_user

from typing import Annotated, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,extract

T_current_user = Annotated[UserModel, Depends(get_current_user)]
T_asyncsession = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter(
    prefix='/monthly_income',
    tags=['Monthly Income'],
)

@router.post("/", response_model=MonthlyIncomePublic, status_code=HTTPStatus.CREATED)
async def create_monthly_income(
    session: T_asyncsession,
    current_user: T_current_user,
    monthly_income: MonthlyIncomeCreate
):
    existing_income = await session.scalar(
        select(MonthlyIncomeModel).where(
            extract('month', MonthlyIncomeModel.initial_date) == monthly_income.initial_date.month,
            extract('year', MonthlyIncomeModel.initial_date) == monthly_income.initial_date.year,
            MonthlyIncomeModel.user_id == current_user.id
        )
    )

    if existing_income:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='There is already a registered monthly income please delete or update.'
        )

    monthly_income_db = MonthlyIncomeModel(**monthly_income.model_dump(), user_id=current_user.id)
    
    session.add(monthly_income_db)
    await session.commit()
    await session.refresh(monthly_income_db)

    return monthly_income_db

@router.get('/', response_model=MonthlyIncomeList)
async def read_monthly_income(
        session: T_asyncsession,
        current_user: T_current_user,
        ):
        result = await session.scalars(
            select(MonthlyIncomeModel).where(MonthlyIncomeModel.user_id == current_user.id)
        )
        monthly_incomes_db = result.all()

        if not monthly_incomes_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Monthly Income not found.'
            )

        return {'monthly_incomes': monthly_incomes_db}


@router.patch('/{monthly_income_id}',response_model=MonthlyIncomePublic)
async def update_monthly_income(
     session:T_asyncsession,
     current_user: T_current_user,
     monthly_income: MonthlyIncomeUpdate,
     monthly_income_id: int
     ):

     monthly_income_db = select(MonthlyIncomeModel).where(MonthlyIncomeModel.id == monthly_income_id)
     monthly_income_obj = await session.scalar(monthly_income_db)
     
     if not monthly_income_obj:
          raise HTTPException(
               status_code=HTTPStatus.NOT_FOUND,
               detail = 'Monthly Income not found.'
          )
     
     if monthly_income_obj.user_id != current_user.id:
          raise HTTPException(
               status_code= HTTPStatus.FORBIDDEN,
               detail= 'Not engough permissions'
          )
     
     for key,value in monthly_income.model_dump(exclude_unset=True).items():
          setattr(monthly_income_obj,key,value)
    
     await session.commit()
     await session.refresh(monthly_income_obj)

     return monthly_income_obj

@router.delete('/{monthly_income_id}')
async def delete_monthly_income(
     session: T_asyncsession,
     current_user: T_current_user,
     monthly_income_id: int,
     ):

     monthly_income_db = select(MonthlyIncomeModel).where(MonthlyIncomeModel.id == monthly_income_id)
     monthly_income_obj = await session.scalar(monthly_income_db)

     if not monthly_income_obj:
          raise HTTPException(
               status_code=HTTPStatus.NOT_FOUND,
               detail= 'Monthly Income not found.'
          )
     
     if monthly_income_obj.user_id != current_user.id:
          raise HTTPException(
               status_code=HTTPStatus.FORBIDDEN,
               detail= 'Not engough permissions'
          )
     
     await session.delete(monthly_income_obj)
     await session.commit()

     return {'message': 'Monthly Income deleted.'}



    







