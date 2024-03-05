from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from sql import schemas, crud

from dependencies import get_db, get_current_active_user


router = APIRouter(prefix="/users")

@router.post('/', response_model=schemas.User)
def create_user(
        db: Annotated[Session, Depends(get_db)], 
        user: schemas.UserCreate
    ):

    try:
        return crud.create_user(db, user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User email/username already exists")

@router.get("/", response_model=list[schemas.User])
def get_users(
        db: Annotated[Session, Depends(get_db)], 
        skip: int = 0, limit: int = 100
    ):

    users = crud.get_users(db, skip, limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def get_user(
        db: Annotated[Session, Depends(get_db)], 
        user_id: int
    ):

    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user

@router.post("/{user_id}", response_model=schemas.User)
def update_user(
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        data: schemas.UserUpdate, user_id: int
    ):

    db_user = crud.update_user(db, user_id, data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user

@router.post("/{user_id}/delete", response_model=schemas.User)
def delete_user(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        user_id: int
    ):

    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user