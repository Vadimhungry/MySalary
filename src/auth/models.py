from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    String,
    func,
    Numeric,
    TIMESTAMP
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class User(SQLAlchemyBaseUserTable[int], BaseModel):
    """User model"""
    __tablename__ = 'user'

    first_name: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False
    )

    salary: Mapped[Numeric] = mapped_column(Numeric(precision=10, scale=2))
    promotion_date: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP)

    email: Mapped[str] = mapped_column(
        String(length=320),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
