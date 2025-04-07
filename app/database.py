from sqlalchemy.orm import sessionmaker, declarative_base 
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession

from app.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)

SessionLocal = AsyncSession(bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    with db as session:
        yield db
    