from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from sql import schemas, crud

from dependencies import get_db, get_current_active_user

router = APIRouter(prefix="/books")

@router.post("/", response_model=schemas.Book)
def create_book(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Security(get_current_active_user, scopes=["super"])],
        book: schemas.BookCreate
    ):

    try:
        return crud.create_book(db, book)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create book")
    
@router.get("/", response_model=list[schemas.Book])
def get_books(
        db: Annotated[Session, Depends(get_db)],
        skip: int = 0, limit: int = 100,
        genre: str = '', language: str = ''
    ):

    if not (genre or language):
        return crud.get_books(db, skip, limit)
    elif genre and language:
        return crud.filter_books_by_language_and_genre(
            db, 
            language, 
            genre,
            skip,
            limit)
    elif genre:
        return crud.get_books_by_genre(db, genre, skip, limit)
    else:
        return crud.get_books_by_language(db, language, skip, limit)

@router.get("/{book_id}", response_model=schemas.Book)
def get_book(
        db: Annotated[Session, Depends(get_db)], 
        book_id: int
    ):

    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book deos not exist")
    return db_book

@router.post("/{book_id}", response_model=schemas.Book)
def update_book(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Security(get_current_active_user, scopes=["super"])],
        book: schemas.BookUpdate, book_id: int
    ):

    db_book = crud.update_book(db, book_id, book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book does not exist")
    return db_book

@router.post("/{book_id}/delete", response_model=schemas.Book)
def delete_book(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Security(get_current_active_user, scopes=["super"])],
        book_id: int
    ):

    db_book = crud.delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book does not exist")
    return db_book