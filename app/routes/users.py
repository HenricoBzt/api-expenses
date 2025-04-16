from http import HTTPStatus

from typing import Annotated

from app.database import get_db
from app.models import UserModel
from app.schemas.user_schema import UserPublic, UserCreate, UserList
from app.security import get_hash_password,get_current_user

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T_asyncsession = Annotated[AsyncSession, Depends(get_db)]
T_CurrentUser = Annotated[UserModel, Depends(get_current_user)]

router = APIRouter(prefix='/users',tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic )
async def create_user(user:UserCreate, session: T_asyncsession):
    stmt = select(UserModel).where((UserModel.username == user.username) | (UserModel.email == user.email))
    user_db = await session.scalar(stmt)
    
    if user_db:
        if user_db.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail= 'Username already exist'
            )
        
        elif user_db.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail= 'Email already exists'
            )
    

    user_db = UserModel(
        username = user.username,
        email = user.email,
        hashed_password = get_hash_password(user.password)
    )

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    return user_db

@router.get('/', response_model= UserList)
async def read_users(session: T_asyncsession,current_user: T_CurrentUser,skip: int = 0, limit: int = 100):
    stmt = select(UserModel).offset(skip).limit(limit)
    user_db = await session.scalars(stmt)

    return {'users': user_db}


@router.put('/{user_id}')
async def update_user(
            session: T_asyncsession,
            user_id: int,
            user: UserCreate,
            current_user: T_CurrentUser):


    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail= 'Not enough permission ')

    current_user.username = user.username
    current_user.email = user.email
    current_user.hashed_password = get_hash_password(user.password)

    await session.commit()
    await session.refresh(current_user)

    return current_user

@router.delete('/{user_id}')
async def delete_user(session: T_asyncsession,
                user_id: int,
                current_user: T_CurrentUser):
    
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, 
                            detail= 'Not enough permission ')
    
    await session.delete(current_user)
    await session.commit()
    return {'message': 'User Deleted'}