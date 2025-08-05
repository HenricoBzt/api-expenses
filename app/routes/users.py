from http import HTTPStatus

from typing import Annotated

from app.database import get_db
from app.models import UserModel
from app.schemas.user_schema import UserPublic, UserCreate, UserList
from app.security import get_current_user

from app.crud.users_crud import (
    create_user,
    list_users,
    list_current_user,
    update_user,
    delete_user,
)

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

T_asyncsession = Annotated[AsyncSession, Depends(get_db)]
T_CurrentUser = Annotated[UserModel, Depends(get_current_user)]

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user_endpoint(user: UserCreate, session: T_asyncsession):

    return await create_user(session=session, user_data=user)


@router.get("/", response_model=UserList)
async def read_users_endpoint(
    session: T_asyncsession,
    current_user: T_CurrentUser,
    skip: int = 0,
    limit: int = 100,
):

    return await list_users(session=session, skip=skip, limit=limit)


@router.get("/me", response_model=UserList)
async def read_current_user(session: T_asyncsession, current_user: T_CurrentUser):
    return await list_current_user(session, current_user)


@router.put("/{user_id}")
async def update_user_endpoint(
    user_id: int, user: UserCreate, session: T_asyncsession, current_user: T_CurrentUser
):

    return await update_user(
        session=session, user_id=user_id, user_data=user, current_user=current_user
    )


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user_endpoint(
    user_id: int, session: T_asyncsession, current_user: T_CurrentUser
):

    return await delete_user(
        session=session, user_id=user_id, current_user=current_user
    )
