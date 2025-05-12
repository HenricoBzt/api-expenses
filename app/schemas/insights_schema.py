from app.schemas.basemodel_config import MyBaseModel
from pydantic import Field
from decimal import Decimal
from datetime import date

class InsightMonthly(MyBaseModel):
    current_income:Decimal= Field(..., ge=0, description="Renda cadastrada no período")
    total_spent:Decimal= Field(..., ge=0, description="Soma das despesas no período")
    remaining_balance:Decimal= Field(..., ge=0, description="Saldo restante (income - spent)")
    percentual_spent:float= Field(..., ge=0, le=100, description="Percentual do orçamento usado")
    year:int= Field(..., ge=2000, le=9999, description="Ano do resumo")
    month:int= Field(..., ge=1,   le=12,   description="Mês do resumo")

 
class CategoryInsightMonthly(MyBaseModel):
    name_category: str = Field(min_length=4,description='Digits')