from app.database import get_db
from app.models import CategoryModel, UserModel
from app.schemas.category_schema import CategoryPublic, CategoryCreate, CategoryList
from app.security import get_current_user

from fastapi import APIRouter, HTTPException, Query, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from http import HTTPStatus

from typing import Annotated, Optional


T_asyncsession = Annotated[AsyncSession, Depends(get_db)]
T_current_user = Annotated[UserModel, Depends(get_current_user)]
T_query = Annotated[Optional[str],Query(min_length= None, description="Procure por categorias")]

router = APIRouter(
    prefix='/category',
    tags=['category']
)

@router.post('/',response_model=CategoryPublic)
async def create_category(
    session: T_asyncsession,
    current_user: T_current_user,
    category: CategoryCreate
    ):

    category_db = CategoryModel(**category.model_dump(),user_id=current_user)

    session.add(category_db)
    await session.commit()
    await session.refresh(category_db)

    return category_db

@router.get('/search/',response_model=CategoryList)
async def read_categories(
    session: T_asyncsession,
    current_user: T_current_user,
    query: T_query = None,
    skip: int = 0,
    limit: int = 10
    ):

    stmt_base = select(CategoryModel).order_by(CategoryModel.name).where(CategoryModel.user_id == current_user.id)
    stmt_query = stmt_base

    if query:
        stmt_query = stmt_base.where(CategoryModel.name.ilike(f'%{query}%'))
    
    stmt_pagined = stmt_query.offset(skip).limit(limit)
   
    result = await session.scalars(stmt_pagined)
    categories_list = result.all()

    return {'categories': categories_list}

@router.put('/{category_id}',response_model=CategoryPublic)
async def update_category(
        session: T_asyncsession,
        current_user: T_current_user,
        category_id: int,
        category: CategoryCreate
        ):
    
    category_stmt = select(CategoryModel).where(
         CategoryModel.id == category_id, 
         CategoryModel.user_id == current_user.id
         )
    
    category_obj = await session.scalar(category_stmt)
    
    if not category_obj:
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND,
            detail= 'Category not found'
        ) 
    
    if category_obj.user_id != current_user.id:
        raise HTTPException(
            status_code = HTTPStatus.FORBIDDEN,
            detail= 'Not engough permissions'
        )
    
    category_obj.name = category.name

    await session.commit()
    await session.refresh(category_obj)
    
    return category_obj

@router.delete('/{category_id}')
async def delete_category(
    session: T_asyncsession,
    current_user: T_current_user,
    category_id: int
    ):
    category_stmt = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.user_id == current_user.id)
    category_obj = await session.scalar(category_stmt)

    if not category_obj:
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND,
            detail= 'Category not found'
        )
    
    if category_obj.user_id != current_user.id:
                raise HTTPException(
                        status_code=HTTPStatus.FORBIDDEN,
                        detail= 'Not enough permission' 
                )
        
    
    await session.delete(category_obj)
    await session.commit()

    return {'detail': 'Category deleted'}

