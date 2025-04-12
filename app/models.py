from sqlalchemy import (
    Column, 
    String, 
    Integer, 
    ForeignKey, 
    Date, 
    Enum, 
    Text,
    Numeric
    )

from sqlalchemy.orm import relationship
from app.database import Base

import enum

class StatusType(enum.Enum):
    PAGO = "pago"
    PENDENTE = "pendente"
    ATRASADO = "atrasado"


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True )
    username = Column(String, nullable=False,unique=True)
    email = Column(String, nullable=False, unique= True)
    hashed_password = Column(String, nullable=False)

    categories = relationship(
        'CategoryModel', 
        back_populates='user',
        cascade = 'all, delete, delete-orphan'
        )
    
    expenses = relationship(
        'ExpensesModel', 
        back_populates='user',
        cascade = 'all, delete, delete-orphan'
        )

class CategoryModel(Base):
    __tablename__ = 'categories'
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("UserModel", back_populates="categories")
    expenses = relationship(
        "ExpensesModel", 
        back_populates="category",
        cascade= 'all, delete, delete-orphan'
        )


class ExpensesModel(Base):
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    title = Column(String(100),nullable=True)
    description = Column(Text(), nullable=True)
    amount = Column(Numeric(10,2), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(StatusType), nullable=False)

    user = relationship("UserModel", back_populates="expenses")
    category = relationship("CategoryModel", back_populates="expenses")
