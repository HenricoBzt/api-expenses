from sqlalchemy.orm import sessionmaker, declarative_base 
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession

from app.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)



Base = declarative_base()

async def get_db():
    async with AsyncSession(bind=engine,expire_on_commit=False) as session:
        yield session
    