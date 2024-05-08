from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Numeric, Column, Integer, TIMESTAMP, VARCHAR, func


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Employee(BaseModel):
    """Employee model"""
    __tablename__ = 'employees'

    first_name = Column(VARCHAR(255), nullable=False)
    last_name = Column(VARCHAR(255), nullable=False)
    login = Column(VARCHAR(255), nullable=False, unique=True)
    password = Column(VARCHAR(255))
    salary = Column(Numeric(precision=10, scale=2))
    promotion_date = Column(TIMESTAMP)
