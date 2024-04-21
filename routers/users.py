from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from sql import schemas, crud

from dependencies import get_db, get_current_active_user


router = APIRouter(prefix="/users")

@router.post('/', response_model=schemas.User, tags=["users"])
def create_user(
        db: Annotated[Session, Depends(get_db)], 
        user: schemas.UserCreate
    ):

    try:
        return crud.create_user(db, user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User email/username already exists")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid email format")

@router.get("/", response_model=list[schemas.UserInline], tags=["users"])
def get_users(
        db: Annotated[Session, Depends(get_db)], 
        skip: int = 0, limit: int = 100
    ):

    users = crud.get_users(db, skip, limit)
    return users

@router.get("/{user_id}", response_model=schemas.User, tags=["users"])
def get_user(
        db: Annotated[Session, Depends(get_db)], 
        user_id: int
    ):

    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user

@router.patch("/me", response_model=schemas.User, tags=["users"])
def update_profile(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Security(get_current_active_user)],
        data: schemas.UserSelfUpdate
    ):
    
    db_user = crud.update_user(db, current_user.id, data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user

@router.patch("/{user_id}", response_model=schemas.User, tags=["admin"])
def update_user(
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[schemas.User, Security(get_current_active_user, scopes=["super"])],
        data: schemas.UserUpdate, user_id: int
    ):

    db_user = crud.update_user(db, user_id, data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user

@router.delete("/{user_id}/delete", response_model=schemas.User, tags=["admin"])
def delete_user(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Security(get_current_active_user, scopes=["super"])],
        user_id: int
    ):

    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user
