from fastapi import FastAPI,Depends, HTTPException
from http import HTTPStatus

from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from models import ExpensesModel
from schemas.expenses_schemas import ExpenseCreate, ExpensePublic, ExpenseList

router = FastAPI(
    prefix='/expenses/',
    tags=['expenses']
)


