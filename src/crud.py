from sqlalchemy.orm import Session
from . import models, schemas


def get_employees(db: Session, limit):
    return db.query(models.Employee).all()[:limit]


def create_employee(db: Session, employee: schemas.Employee):
    db_employee = models.Employee(
        first_name=employee.first_name,
        login=employee.login,
        last_name=employee.last_name,
        password=employee.password,
        salary=employee.salary,
        promotion_date=employee.promotion_date
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employee_by_login(db: Session, login: str):
    return db.query(models.Employee).filter(models.Employee.login == login).first()


def get_employee_by_id(db: Session, id: int):
    return db.query(models.Employee).filter(models.Employee.id == id).first()


def update_employee(db: Session, id: int, employee_data: schemas.Employee):
    db_employee = db.query(models.Employee).filter(models.Employee.id == id).first()

    db_employee.first_name = employee_data.first_name
    db_employee.last_name = employee_data.last_name
    db_employee.login = employee_data.login
    db_employee.password = employee_data.password
    db_employee.salary = employee_data.salary
    db_employee.promotion_date = employee_data.promotion_date

    db.commit()
    db.refresh(db_employee)

    return db_employee


def delete_employee(db, db_employee):
    db.delete(db_employee)
    db.commit()
    return db_employee
