from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from typing import Annotated
from datetime import timedelta

from sql import crud, models, schemas
from sql.database import engine
import dependencies
from dependencies import get_db, get_current_active_user
from routers.users import router as users_router
from routers.books import router as books_router
from routers.authors import router as authors_router
from routers.genres import router as genres_router

models.Base.metadata.create_all(bind=engine)

def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not dependencies.check_password(password, user.hashed_password):
        return False
    return user

app = FastAPI()

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

# language
@app.post("/languages/", response_model=schemas.Language)
def create_language(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        language: schemas.LanguageCreate
    ):

    try:
        return crud.create_language(db, language)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create language")
    
@app.get("/languages/", response_model=list[schemas.Language])
def get_languages(
        db: Annotated[Session, Depends(get_db)], 
        skip: int = 0, limit: int = 100
    ):

    return crud.get_languages(db, skip, limit)

@app.post("/languages/{language_id}", response_model=schemas.Language)
def update_language(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        language: schemas.LanguageUpdate, language_id: int
    ):

    db_language = crud.update_language(db, language_id, language)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language does not exist")
    return db_language

@app.post("/languages/{language_id}/delete", response_model=schemas.Language)
def delete_language(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        language_id: int
    ):

    db_language = crud.delete_language(db, language_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language does not exist")
    return db_language

app.include_router(books_router)

# book instance
@app.post("/bookinstances/", response_model=schemas.BookInstance)
def create_bookinstance(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        instance: schemas.BookInstanceCreate
    ):

    try:
        return crud.create_book_instance(db, instance)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create book instance")
    
@app.get("/bookinstances/", response_model=list[schemas.BookInstance])
def get_bookinstances(
        db: Annotated[Session, Depends(get_db)], 
        skip: int = 0, limit: int = 100
    ):

    return crud.get_book_instances(db, skip, limit)

@app.get("/bookinstances/{instance_id}", response_model=schemas.BookInstance)
def get_bookinstance(
        db: Annotated[Session, Depends(get_db)], 
        instance_id: str
    ):

    db_bookinstance = crud.get_book_instance(db, instance_id)
    if db_bookinstance is None:
        raise HTTPException(status_code=404, detail="Book instance deos not exist")
    return db_bookinstance

@app.post("/bookinstances/{instance_id}", response_model=schemas.BookInstance)
def update_bookinstance(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        instance: schemas.BookInstanceUpdate, instance_id: str
    ):
    
    db_bookinstance = crud.update_book_instance(db, instance_id, crud)
    if db_bookinstance is None:
        raise HTTPException(status_code=404, detail="Book instance does not exist")
    return db_bookinstance

@app.post("/bookinstances/{instance_id}/delete", response_model=schemas.BookInstance)
def delete_bookinstance(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)], 
        instance_id: str
    ):

    db_bookinstance = crud.delete_book_instance(db, instance_id)
    if db_bookinstance is None:
        raise HTTPException(status_code=404, detail="Book does not exist")
    return db_bookinstance