from main import app
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.auth.models import BaseModel
from src.auth.models import User
from src.auth.schemas import UserCreate
from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from fastapi_users import FastAPIUsers
from fastapi import Depends
import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from src.db import get_async_session


DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@app.get("/protected-route")
async def protected_route(user: User = Depends(fastapi_users.current_user(active=True))):
    return {"message": "Success"}


@pytest.fixture
async def async_client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
async def setup_db():
    # Create the tables before each test
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield  # Run the test

    # Drop the tables after each test
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.mark.asyncio
async def test_login_user(async_client, setup_db):
    # Регистрация пользователя перед логином
    register_response = await async_client.post(
        "/auth/register",
        json={
            "first_name": "xgh1mzabn51pokjbvzmajrmvovo",
            "last_name": "xgh1mzabn51pokjbvzmajrmvova",
            "salary": 1000.50,
            "promotion_date": "2024-05-30",
            "email": "xgh1mzabn51pokjbvzmajrmvovi@example.com",
            "password": "xgh1mzabn51pokjbvzmajrmvove",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False
        }
    )
    users = await async_client.get("/users")
    print('|||||||')
    print(users.content)
    assert register_response.status_code == 201

