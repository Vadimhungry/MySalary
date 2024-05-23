from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from typing import AsyncGenerator

# get env variables
load_dotenv()
db_url = DATABASE_URL = os.getenv('DB_LINK')

# engine = create_engine(
#     db_url, echo=True
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# connection = engine.connect()

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session