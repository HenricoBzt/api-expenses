from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional
import datetime
from app.models import StatusType 

class MyBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

class ExpenseCreate(MyBaseModel):
    category_id: int
    title: str
    description: str
    amount: float
    date: datetime.date
    status: StatusType

class ExpensePublic(ExpenseCreate):
    pass

class ExpenseList(MyBaseModel):
    expenses: list[ExpensePublic]

class ExpenseUpdate(MyBaseModel):
    category_id: int 
    title: str
    description: str | None = None
    amount: float | None = None
    date: datetime.date | None = None
    status: StatusType | None = None

    