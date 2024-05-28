from fastapi import FastAPI, HTTPException
from . import crud, schemas
from sqlalchemy.orm import Session
from .db import SessionLocal, get_async_session
from fastapi import Depends
from .auth.auth import auth_backend
from .auth.schemas import UserRead, UserCreate
from src.auth.models import User
from .auth.manager import get_user_manager
from fastapi_users import FastAPIUsers


app = FastAPI()
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_active_user = fastapi_users.current_user(active=True)


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


@app.get("/users")
async def read_users(
        limit: int = 10,
        db: Session = Depends(get_async_session)
):
    users = await crud.get_users(db, limit)
    return users


@app.post('/users/{id}/delete/', response_model=schemas.User)
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = await crud.get_user_by_id(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await crud.delete_user(db, db_user)
    return db_user


@app.get('/users/{id}', response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = await crud.get_user_by_id(db, id=id)
    return user


@app.get("/my-salary")
def protected_route(user: User = Depends(current_active_user)):
    return (f"Your salary: {user.salary}\n"
            f"Your promotion date: {user.promotion_date}")
