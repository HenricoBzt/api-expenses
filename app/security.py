
from datetime import datetime,timedelta, timezone
from http import HTTPStatus

from jwt import encode, decode
from jwt.exceptions import PyJWTError, DecodeError, ExpiredSignatureError
from pwdlib import PasswordHash

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import UserModel
from app.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')
settings =  Settings()

T_asyncsession = Annotated[AsyncSession, Depends(get_db)]


def get_hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#Funçao para gerar o token JWT 
def generation_access_token(data_payload:dict):
    to_encode = data_payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode,settings.SECRET_KEY,settings.ALGORITHM)
    return encoded_jwt

#Autenticação do usuário
async def get_current_user(
    session: T_asyncsession,
    token: str = Depends(oauth2_scheme)
    ):
    credentials_exception = HTTPException(
        status_code= HTTPStatus.UNAUTHORIZED,
        detail= 'Could not validate credentials',
        headers= {'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = decode(token,settings.SECRET_KEY,settings.ALGORITHM)
        subject_email: str = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except ExpiredSignatureError: 
        raise credentials_exception

    except PyJWTError:
        raise credentials_exception
    
    
    
    user_db = await session.scalar(select(UserModel).where(UserModel.email == subject_email))
    if not user_db:
        raise credentials_exception 

    return user_db




 