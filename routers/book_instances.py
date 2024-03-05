from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from sql import schemas, crud

from dependencies import get_db, get_current_active_user

router = APIRouter(prefix="/bookinstances")


@router.post("/", response_model=schemas.BookInstance)
def create_bookinstance(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        instance: schemas.BookInstanceCreate
    ):

    try:
        return crud.create_book_instance(db, instance)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create book instance")
    
@router.get("/", response_model=list[schemas.BookInstance])
def get_bookinstances(
        db: Annotated[Session, Depends(get_db)], 
        skip: int = 0, limit: int = 100
    ):

    return crud.get_book_instances(db, skip, limit)

@router.get("/{instance_id}", response_model=schemas.BookInstance)
def get_bookinstance(
        db: Annotated[Session, Depends(get_db)], 
        instance_id: str
    ):

    db_bookinstance = crud.get_book_instance(db, instance_id)
    if db_bookinstance is None:
        raise HTTPException(status_code=404, detail="Book instance deos not exist")
    return db_bookinstance

@router.post("/{instance_id}", response_model=schemas.BookInstance)
def update_bookinstance(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        instance: schemas.BookInstanceUpdate, instance_id: str
    ):
    
    db_bookinstance = crud.update_book_instance(db, instance_id, crud)
    if db_bookinstance is None:
        raise HTTPException(status_code=404, detail="Book instance does not exist")
    return db_bookinstance

@router.post("/{instance_id}/delete", response_model=schemas.BookInstance)
def delete_bookinstance(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)], 
        instance_id: str
    ):

    db_bookinstance = crud.delete_book_instance(db, instance_id)
    if db_bookinstance is None:
        raise HTTPException(status_code=404, detail="Book does not exist")
    return db_bookinstance