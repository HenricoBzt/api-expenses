from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.schemas.monthlyincome_schema import MonthlyIncomeUpdate
from app.schemas.expenses_schemas import ExpenseCreate

from app.crud.expenses_crud import (
    create_expense,
    update_expenses,
    delete_expense
)

from app.crud.monthlyincome_crud import (
      get_monthly_income, 
      update_monthlyincome,
      )

from app.models import (
      UserModel,
      StatusType,
      ExpensesModel
      )

async def create_expense_and_update_income(
    session: AsyncSession,
    current_user: UserModel,
    expense_data: ExpenseCreate
):
    try:
        expense = await create_expense(session,current_user,expense_data)

      
        monthly_income = await get_monthly_income(session, current_user)

        if monthly_income and expense_data.status == StatusType.PAGO:
            new_balance = monthly_income.net_balance - expense_data.amount
            monthly_income_update = MonthlyIncomeUpdate(
                net_balance=new_balance,
                initial_date=monthly_income.initial_date,
                user_id=current_user.id
            )
            await update_monthlyincome(
                session,
                current_user,
                monthly_income.id,
                monthly_income_update
            )
        return expense

    except Exception as e:
        print(f"Error: {e}")
        raise


async def update_expense_and_update_income(
    session: AsyncSession,
    current_user: UserModel,
    expense_id: int,
    expense_data: ExpenseCreate
):
    try:
        stmt = select(ExpensesModel).where(
            ExpensesModel.id == expense_id,
            ExpensesModel.user_id == current_user.id
        )
        obj_expense = await session.scalar(stmt)

        if not obj_expense:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='expense not found.'
            )

        monthly_income = await get_monthly_income(session, current_user)
        if not monthly_income:
            return await update_expenses(session, current_user, expense_id, expense_data)

        
        if obj_expense.status != expense_data.status:
            if obj_expense.status == StatusType.PAGO and expense_data.status != StatusType.PAGO:
                monthly_income.net_balance += obj_expense.amount
            elif obj_expense.status != StatusType.PAGO and expense_data.status == StatusType.PAGO:
                monthly_income.net_balance -= expense_data.amount

        elif (
            obj_expense.status == StatusType.PAGO and
            expense_data.status == StatusType.PAGO and
            obj_expense.amount != expense_data.amount
        ):
    
            difference = expense_data.amount - obj_expense.amount
            if (monthly_income.net_balance - difference) < 0:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Insufficient balance.'
                )
            monthly_income.net_balance -= difference

        monthly_income_update = MonthlyIncomeUpdate(
            net_balance=monthly_income.net_balance,
            initial_date=monthly_income.initial_date,
            user_id=current_user.id
        )
        await update_monthlyincome(
            session,
            current_user,
            monthly_income.id,
            monthly_income_update
        )

        updated_expense = await update_expenses(session, current_user, expense_id, expense_data)
        return updated_expense

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the expense."
        )
            
async def delete_expense_and_update_income(
        session:AsyncSession,
        current_user: UserModel,
        expense_id:int,
        ):
            try: 
                stmt = select(ExpensesModel).where(
                         ExpensesModel.id == expense_id,
                         ExpensesModel.user_id == current_user.id
                         )
                
                obj_expense = await session.scalar(stmt)

                if not obj_expense:
                    raise HTTPException(
                        status_code=HTTPStatus.NOT_FOUND,
                        detail='Expense not found.'
                    )
                
                if obj_expense.status == StatusType.PAGO:
                     monthly_income = await get_monthly_income(session, current_user)

                     if not monthly_income:
                            raise HTTPException(
                                status_code=HTTPStatus.NOT_FOUND,
                                detail='Monthly income not found.'
                            )
                     
                     monthly_income.net_balance += obj_expense.amount
                     monthly_income_update = MonthlyIncomeUpdate(
                         net_balance=monthly_income.net_balance,
                         initial_date=monthly_income.initial_date,
                         user_id=current_user.id
                     )

                     await update_monthlyincome(
                         session,
                         current_user,
                         monthly_income.id,
                         monthly_income_update
                     )
                
                return await delete_expense(session, current_user, expense_id)
            
            except Exception as e:
                print(f"Error: {e}")
                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                    detail="An error occurred while deleting the expense."
                )



