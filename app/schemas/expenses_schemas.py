from pydantic import Field
from datetime import date as dt
from decimal import Decimal
from app.models import StatusType 
from app.schemas.basemodel_config import MyBaseModel

class ExpenseCreate(MyBaseModel):
    category_id: int
    title: str
    description: str
    amount: Decimal = Field(gt=0, description='Expense value ')
    date: dt = Field(default_factory=dt.today)
    status: StatusType

class ExpensePublic(ExpenseCreate):
    pass

class ExpenseList(MyBaseModel):
    expenses: list[ExpensePublic]

class ExpenseUpdate(ExpenseCreate):
    pass

    