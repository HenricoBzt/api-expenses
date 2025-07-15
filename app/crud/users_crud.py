from fastapi import HTTPException, Depends
from http import HTTPStatus
from sqlalchemy import select
from app.models import UserModel
from app.schemas.user_schema import UserCreate, UserList
from app.security import get_hash_password
from app.security import get_current_user
from typing import Annotated

T_current_user = Annotated[UserModel, Depends(get_current_user)]


async def create_user(session, user_data: UserCreate):
    stmt = select(UserModel).where(
        (UserModel.username == user_data.username)
        | (UserModel.email == user_data.email)
    )

    existing_user = await session.scalar(stmt)

    if existing_user:
        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Username already exist"
            )
        elif existing_user.email == user_data.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Email already exist"
            )

    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_hash_password(user_data.password),
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def list_users(session, skip: int, limit: int):
    stmt = select(UserModel).offset(skip).limit(limit)
    user_db = await session.scalars(stmt)

    return {"users": user_db}

async def list_current_user(session,current_user: T_current_user):
    stmt = select(UserModel).where(UserModel.id == current_user.id)
    user_obj = await session.scalars(stmt)

    return {"users": user_obj}


async def update_user(
    session, user_id: int, user_data: UserCreate, current_user: T_current_user
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission "
        )

    current_user.username = user_data.username
    current_user.email = user_data.email
    current_user.hashed_password = get_hash_password(user_data.password)

    await session.commit()
    await session.refresh(current_user)

    return current_user


async def delete_user(session, user_id: int, current_user: T_current_user):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission "
        )

    await session.delete(current_user)
    await session.commit()

    return {"message": "User Deleted"}
