from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from typing import Annotated
from datetime import timedelta
import json

from sql import crud, models, schemas, database
from sql.database import engine
import dependencies
from dependencies import get_db, get_current_active_user
from routers.users import router as users_router
from routers.books import router as books_router
from routers.authors import router as authors_router
from routers.genres import router as genres_router
from routers.languages import router as langauges_router
from routers.book_instances import router as book_instances_router

from contextlib import asynccontextmanager

models.Base.metadata.create_all(bind=engine)

def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not dependencies.check_password(password, user.hashed_password):
        return False
    return user

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = database.SessionLocal()
    try:
        with open(".env", "r") as env_file:
            file_dict = json.loads(env_file.read())
            SUPER_USER_USERNAME = file_dict['super_user_username']
            SUPER_USER_PASSWORD = file_dict['super_user_password']
            SUPER_USER_EMAIL = file_dict['super_user_email']
        superuser_count = db.query(models.User).filter(models.User.is_superuser == True).count()
        if superuser_count == 0:
            super_user_schema = schemas.UserCreate(
                username=SUPER_USER_USERNAME, 
                password=SUPER_USER_PASSWORD, 
                email=SUPER_USER_EMAIL)
            super_user = crud.create_user(db, super_user_schema)
            super_user.is_superuser = True
            db.commit()
    finally:
        db.close()
    yield
    #nothing

app = FastAPI(lifespan=lifespan)

@app.get('/')
async def index():
    return {"msg": "Welcome!"}

@app.post("/token")
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[Session, Depends(get_db)]
    ):

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={'WWW-Authenticate': "Bearer"},
        )
    access_token_expires = timedelta(minutes=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = dependencies.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
        )
    return {"access_token": access_token, "token_type":"bearer"}

@app.get("/users/me/", response_model=schemas.User)
def get_current_logged_in_user(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)]
    ):

    return current_user

app.include_router(users_router)
app.include_router(authors_router)
app.include_router(genres_router)
app.include_router(langauges_router)
app.include_router(books_router)
app.include_router(book_instances_router)