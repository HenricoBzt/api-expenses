from app.database import get_db
from app.models import CategoryModel, UserModel
from app.schemas.category_schema import CategoryPublic, CategoryCreate, CategoryList
from app.security import get_current_user
from app.crud.category_crud import (
    create_category,
    read_categories,
    update_category,
    delete_category,
)
from fastapi import APIRouter, HTTPException, Query, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from http import HTTPStatus

from typing import Annotated, Optional


T_asyncsession = Annotated[AsyncSession, Depends(get_db)]
T_current_user = Annotated[UserModel, Depends(get_current_user)]
T_query = Annotated[
    Optional[str], Query(min_length=None, description="Procure por categorias")
]

router = APIRouter(prefix="/category", tags=["category"])


@router.post("/", response_model=CategoryPublic)
async def create_category(
    session: T_asyncsession, current_user: T_current_user, category_data: CategoryCreate
):
    return await create_category(session, current_user, category_data)


@router.get("/", response_model=CategoryList)
async def get_categories(
    session: T_asyncsession,
    current_user: T_current_user,
    query: T_query = None,
    skip: int = 0,
    limit: int = 10,
):

    return await read_categories(
        session,
        current_user,
        query=query,
        skip=skip,
        limit=limit,
    )


@router.put("/{category_id}", response_model=CategoryPublic)
async def update_category(
    session: T_asyncsession,
    current_user: T_current_user,
    category_id: int,
    category: CategoryCreate,
):

    return await update_category(
        session,
        current_user,
        category_id,
        category,
    )


@router.delete("/{category_id}")
async def delete_category(
    session: T_asyncsession, current_user: T_current_user, category_id: int
):
    return await delete_category(
        session,
        current_user,
        category_id,
    )
