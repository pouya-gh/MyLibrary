from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from sql import schemas, crud

from dependencies import get_db, get_current_active_user

from datetime import timedelta, datetime

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

@router.post("/{instance_id}/borrow", response_model=schemas.BookInstance)
def borrow_book(
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        instance_id: str
    ):

    instance_db = crud.get_book_instance(db, instance_id)
    if instance_db is None:
        raise HTTPException(status_code=404, detail="Book instance not found")
    
    if instance_db.status == schemas.BookInstanceStatus.a:
        update_data = schemas.BookInstanceUpdate(
            status=schemas.BookInstanceStatus.o,
            borrower_id=current_user.id,
            due_back=datetime.today().date() + timedelta(days=14))
        return crud.update_book_instance(db, instance_id, update_data)
    else:
        raise HTTPException(status_code=400, detail="Book instance is not available")

@router.post("/{instance_id}/return", response_model=schemas.BookInstance) 
def return_book(
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        instance_id: str
    ):

    instance_db = crud.get_book_instance(db, instance_id)
    if instance_db is None:
        raise HTTPException(status_code=404, detail="Book instance not found")
    
    if instance_db.status == schemas.BookInstanceStatus.o and \
        instance_db.borrower_id == current_user.id:
        update_data = schemas.BookInstanceUpdate(
            status=schemas.BookInstanceStatus.a,
            borrower_id=0)
        return crud.update_book_instance(db, instance_id, update_data)
    else:
        raise HTTPException(status_code=400, detail="This book instance is not borrowed to you")