from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.security import get_current_user
from app.schemas.classifier_schema import ExpenseClassifierRequest, ExpenseClassifierResponse
from app.services.ai_classifier import classify_expense
from app.models import UserModel
from typing import Annotated

router = APIRouter(prefix="/classifier", tags=["Classifier"])

T_asyncsession = Annotated[AsyncSession, Depends(get_db)]
T_current_user = Annotated[UserModel, Depends(get_current_user)]


@router.post("/expense", response_model=ExpenseClassifierResponse)
async def classify_expense_endpoint(
    body: ExpenseClassifierRequest,
    session: T_asyncsession,
    current_user: T_current_user
):
    category = await classify_expense(description=body.description)
    return ExpenseClassifierResponse(suggested_category=category)
