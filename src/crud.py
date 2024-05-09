from sqlalchemy.orm import Session
from . import schemas
from .auth import models


def get_users(db: Session, limit):
    return db.query(models.User).all()[:limit]


# def create_employee(db: Session, employee: schemas.User):
#     db_employee = models.User(
#         first_name=employee.first_name,
#         last_name=employee.last_name,
#         login=employee.login,
#         salary=employee.salary,
#         promotion_date=employee.promotion_date,
#         email=employee.email,
#         hashed_password=employee.hashed_password,
#         is_active=employee.is_active,
#         is_superuser=employee.is_superuser,
#         is_verified=employee.is_verified
#     )
#     db.add(db_employee)
#     db.commit()
#     db.refresh(db_employee)
#     return db_employee

def get_employee_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def update_user(db: Session, id: int, user_data: schemas.User):
    db_employee = db.query(models.User).filter(models.User.id == id).first()

    db_employee.first_name = user_data.first_name
    db_employee.last_name = user_data.last_name
    db_employee.username = user_data.username
    db_employee.password = user_data.password
    db_employee.salary = user_data.salary
    db_employee.promotion_date = user_data.promotion_date

    db.commit()
    db.refresh(db_employee)

    return db_employee


def delete_user(db, db_employee):
    db.delete(db_employee)
    db.commit()
    return db_employee
