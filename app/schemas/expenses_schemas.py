from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional
import datetime

from app.models import StatusType 
from app.schemas.basemodel_config import MyBaseModel

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

class ExpenseUpdate(ExpenseCreate):
    pass

    