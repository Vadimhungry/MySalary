from fastapi_users import schemas
from pydantic import EmailStr
from typing import Optional
import datetime


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    salary: float
    promotion_date: Optional[datetime.date]

    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True


class UserUpdate(schemas.BaseUserUpdate):
    pass
