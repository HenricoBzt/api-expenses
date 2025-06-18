from fastapi import HTTPException, Depends
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from typing import Annotated

from app.models import CategoryModel, UserModel

from app.security import get_current_user

from app.schemas.category_schema import CategoryCreate, CategoryPublic, CategoryList


# Function to create a new category
async def create_category(
    session: AsyncSession, category_data: CategoryCreate, current_user: UserModel
):
    new_category = CategoryModel(**category_data.model_dump(), user_id=current_user.id)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category


# Function to read categories with optional search query
async def read_categories(
    session: AsyncSession,
    current_user: UserModel,
    query: str = None,
    skip: int = 0,
    limit: int = 10,
):

    stmt_base = (
        select(CategoryModel)
        .order_by(CategoryModel.name)
        .where(CategoryModel.user_id == current_user.id)
    )
    stmt_query = stmt_base

    if query:
        stmt_query = stmt_base.where(CategoryModel.name.ilike(f"%{query}%"))

    stmt_pagined = stmt_query.offset(skip).limit(limit)

    result = await session.scalars(stmt_pagined)
    categories_list = result.all()

    if not categories_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Category not found."
        )

    return {"categories": categories_list}


# Function to update a category by ID
async def update_category(
    session: AsyncSession,
    current_user: UserModel,
    category_id: int,
    category_data: CategoryCreate,
):
    category_stmt = select(CategoryModel).where(
        CategoryModel.id == category_id, CategoryModel.user_id == current_user.id
    )

    category_obj = await session.scalar(category_stmt)

    if not category_obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Category not found."
        )

    for key, value in category_data.model_dump().items():
        setattr(category_obj, key, value)

    session.add(category_obj)
    await session.commit()
    await session.refresh(category_obj)

    return category_obj


# Function to delete a category by ID
async def delete_category(
    session: AsyncSession, current_user: UserModel, category_id: int
):
    category_stmt = select(CategoryModel).where(
        CategoryModel.id == category_id, CategoryModel.user_id == current_user.id
    )

    category_obj = await session.scalar(category_stmt)

    if not category_obj:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Category not found."
        )

    await session.delete(category_obj)
    await session.commit()

    return {"detail": "Category deleted successfully."}

