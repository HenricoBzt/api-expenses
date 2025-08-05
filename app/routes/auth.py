from http import HTTPStatus

from app.models import UserModel
from app.security import verify_password, generation_access_token, get_current_user
from app.database import get_db
from app.schemas.user_schema import Token

from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/auth", tags=["auth"])

T_asyncsession = Annotated[AsyncSession, Depends(get_db)]
T_formdata = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: T_formdata, session: T_asyncsession):
    stmt = select(UserModel).where(UserModel.email == form_data.username)

    user_db = await session.scalar(stmt)

    if not user_db or not verify_password(form_data.password, user_db.hashed_password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="password or email incorrect"
        )

    access_token = generation_access_token({"sub": user_db.email})

    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/refresh_token", response_model=Token)
async def refresh_token(user: UserModel = Depends(get_current_user)):
    new_access_token = generation_access_token({"sub": user.email})

    return {"access_token": new_access_token, "token_type": "Bearer"}
