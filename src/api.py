from fastapi import FastAPI, HTTPException
from . import crud, models, schemas
from sqlalchemy.orm import Session
from .db import SessionLocal
from fastapi import Depends
from .auth.auth import auth_backend
from .auth.schemas import UserRead, UserCreate
from .auth.database import User
from .auth.manager import get_user_manager
from fastapi_users import FastAPIUsers


app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


# @app.post('/users/', response_model=schemas.User)
# def create_employee(employee: schemas.User, db: Session = Depends(get_db)):
#     ''''''
#     db_employee = crud.get_employee_by_login(db, login=employee.login)
#     if db_employee:
#         raise HTTPException(status_code=400, detail="Login already registered")
#     return crud.create_employee(db=db, employee=employee)



@app.get('/users/', response_model=list[schemas.AllUsers])
def get_users(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, limit=limit)


@app.post('/users/{id}/delete/', response_model=schemas.User)
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, db_user)
    return db_user

@app.post('/users/{id}', response_model=schemas.User)
def update_user(id: int, user: schemas.User, db: Session = Depends(get_db)):
    return crud.update_user(db=db, id=id, user_data=user)


@app.get('/users/{id}', response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, id=id)
