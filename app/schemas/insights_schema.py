from app.schemas.basemodel_config import MyBaseModel
from pydantic import Field
from decimal import Decimal
from typing import List


class InsightMonthly(MyBaseModel):
    current_income: Decimal = Field(
        ..., ge=0, description="Renda cadastrada no período"
    )
    total_spent: Decimal = Field(..., ge=0, description="Soma das despesas no período")
    remaining_balance: Decimal = Field(
        ..., ge=0, description="Saldo restante (income - spent)"
    )
    percentual_spent: float = Field(
        ..., ge=0, le=100, description="Percentual do orçamento usado"
    )
    year: int = Field(..., ge=2000, le=9999, description="Ano do resumo")
    month: int = Field(..., ge=1, le=12, description="Mês do resumo")


class ExpenseByCategoryItem(MyBaseModel):
    category_id: int
    category_name: str
    total_expenses: Decimal = Field(..., ge=0)


class CategoryInsightMonthly(MyBaseModel):
    expenses_by_category: List[ExpenseByCategoryItem]
