from http import HTTPStatus

from app.models import UserModel
from app.security import  verify_password, generation_access_token
from app.database import get_db
from app.schemas.user_schema import UserCreate, Token

from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session



router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[Session,Depends(get_db)] 
T_formdata = Annotated[OAuth2PasswordRequestForm,Depends()]

@router.post('/', response_model=Token)
def login_for_access_token(form_data:T_formdata ,session: T_Session):
    stmt = select(UserModel).where(UserModel.username == form_data.username)

    user_db = session.scalar(stmt)

    if not user_db or not verify_password(form_data.password, user_db.hashed_password):
        raise HTTPException(
            status_code = HTTPStatus.BAD_REQUEST,
            detail = 'password or email incorrect'
        )
    
    access_token = generation_access_token({'sub': user_db.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
    
