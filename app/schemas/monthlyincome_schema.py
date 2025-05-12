from pydantic import Field
from app.schemas.basemodel_config import MyBaseModel
from datetime import date

class MonthlyIncomeCreate(MyBaseModel):
    net_balance: int = Field(gt=0,description='Renda mensal') 
    initial_date: date = Field(default_factory=date.today)

class MonthlyIncomePublic(MonthlyIncomeCreate):
    pass

class MonthlyIncomeList(MyBaseModel):
    monthly_incomes: list[MonthlyIncomePublic]
    
class MonthlyIncomeUpdate(MonthlyIncomeCreate):
    pass


