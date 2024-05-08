from pydantic import BaseModel
from datetime import datetime


class Employee(BaseModel):
    id: int
    first_name: str
    last_name: str
    login: str
    password: str
    salary: float
    promotion_date: datetime
