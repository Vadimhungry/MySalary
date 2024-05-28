from main import app  # Импортируйте ваш FastAPI app
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_async_session
from src.auth.models import User
from src.auth.schemas import UserCreate
from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import BaseModel
from fastapi_users import FastAPIUsers
from fastapi import Depends
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройки для тестовой базы данных
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Создаем экземпляр FastAPIUsers для тестирования
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


# Добавляем защищенный маршрут для тестирования
@app.get("/protected-route")
async def protected_route(user: User = Depends(fastapi_users.current_user(active=True))):
    return {"message": "Success"}


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.mark.asyncio
async def test_register_and_login_user(async_client, setup_db):
    # Регистрация нового пользователя
    register_response = await async_client.post(
        "/auth/register",
        json={
            "first_name": "Arkasha",
            "last_name": "Aboltus",
            "salary": 111.222,
            "promotion_date": "2025-11-22T00:00:00",
            "email": 'aboltus@mail.ru',
            "password": "test_pass_1",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        }
    )

    print("Registration failed:", register_response.json())
    assert register_response.status_code == 201
    #
    # # Выполнение входа для получения токена
    # login_response = await async_client.post(
    #     "/auth/jwt/login",
    #     data={
    #         "username": "aboltus@mail.ru",
    #         "password": "test_pass_1"
    #     },
    #     headers={"Content-Type": "application/x-www-form-urlencoded"}
    # )
    # assert login_response.status_code == 200
    # tokens = login_response.json()
    # assert "access_token" in tokens
    #
    # access_token = tokens["access_token"]
    #
    # # Использование токена для доступа к защищенному маршруту
    # headers = {"Authorization": f"Bearer {access_token}"}
    # protected_response = await async_client.get("/protected-route", headers=headers)
    # assert protected_response.status_code == 200
    # assert protected_response.json() == {"message": "Success"}
