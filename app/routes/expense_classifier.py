from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.security import get_current_user
from app.models import UserModel
from typing import Annotated
from app.schemas.classifier_schema import ExpenseClassifierRequest, ExpenseClassifierResponse
from app.services.ai_classifier import classify_expense

router = APIRouter(
    prefix="/classifier",
    tags=["Classifier"]
)

T_asyncsession = Annotated[AsyncSession, Depends(get_db)]
T_current_user = Annotated[UserModel, Depends(get_current_user)]

@router.post(
    "/expense",
    response_model=ExpenseClassifierResponse,
    summary="Classifica descrição de despesa em categoria"
)
async def classify_expense_endpoint(
    body: ExpenseClassifierRequest,
    session: T_asyncsession,
    current_user: T_current_user
):

    category = await classify_expense(description=body.description)
    return ExpenseClassifierResponse(suggested_category=category)
