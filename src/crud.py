from sqlalchemy.orm import Session
from . import schemas
from .auth import models
from sqlalchemy import select


async def get_users(db: Session, limit: int = 10):
    result = await db.execute(select(models.User).limit(limit))
    return result.scalars().all()


async def get_user_by_id(db: Session, id: int):
    result = await db.execute(select(models.User).where(models.User.id == id))
    return result.scalars().first()


# def update_user(db: Session, id: int, user_data: schemas.User):
#     db_employee = db.query(models.User).filter(models.User.id == id).first()
#
#     db_employee.first_name = user_data.first_name
#     db_employee.last_name = user_data.last_name
#     db_employee.username = user_data.username
#     db_employee.password = user_data.password
#     db_employee.salary = user_data.salary
#     db_employee.promotion_date = user_data.promotion_date
#
#     db.commit()
#     db.refresh(db_employee)
#
#     return db_employee


# async def delete_user(db, db_employee):
#     await db.delete(db_employee)
#     db.commit()
#     return db_employee

# async def delete_user(db: Session, db_employee: models.User):
#     await db.delete(db_employee)
#     await db.commit()

async def delete_user(db: Session, db_user: models.User):
    await db.delete(db_user)
    await db.commit()
