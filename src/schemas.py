from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    salary: float
    promotion_date: datetime
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

class AllUsers(User):
    id: int

