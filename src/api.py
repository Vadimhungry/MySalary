from fastapi import FastAPI, HTTPException
from . import crud, models, schemas
from sqlalchemy.orm import Session
from .db import SessionLocal
from fastapi import Depends


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post('/employees/', response_model=schemas.Employee)
def create_employee(employee: schemas.Employee, db: Session = Depends(get_db)):
    db_employee = crud.get_employee_by_login(db, login=employee.login)
    if db_employee:
        raise HTTPException(status_code=400, detail="Login already registered")
    return crud.create_employee(db=db, employee=employee)



@app.get('/employees/', response_model=list[schemas.Employee])
def get_employees(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_employees(db, limit=limit)


@app.post('/employees/{id}/delete/', response_model=schemas.Employee)
def delete_employee(id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee_by_id(db, id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    crud.delete_employee(db, db_employee)
    return db_employee

@app.post('/employees/{id}', response_model=schemas.Employee)
def update_employee(id: int, employee: schemas.Employee, db: Session = Depends(get_db)):

    return crud.update_employee(db=db, id=id, employee_data=employee)


@app.get('/employees/{id}', response_model=schemas.Employee)
def get_employee(id: int, db: Session = Depends(get_db)):
    return crud.get_employee_by_id(db, id=id)
