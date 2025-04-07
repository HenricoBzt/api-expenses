from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional
from datetime import date
from app.models import StatusType 

class MyBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

class ExpenseCreate(MyBaseModel):
    id: int
    user_id: int
    category_id: int
    description: str
    amount: float
    date: date
    status: StatusType

class ExpensePublic(ExpenseCreate):
    pass

class ExpenseList(MyBaseModel):
    expenses: list[ExpensePublic]
    