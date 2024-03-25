from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from sql import schemas, crud

from dependencies import get_db, get_current_active_user

router = APIRouter(prefix="/authors")

@router.post("/", response_model=schemas.Author)
def create_author(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Security(get_current_active_user, scopes=["super"])],
        author: schemas.AuthorCreate
    ):

    try:
        return crud.create_author(db, author)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create author")
    
@router.get("/", response_model=list[schemas.Author])
def get_authors(
        db: Annotated[Session, Depends(get_db)], 
        skip: int = 0, limit: int = 100
    ):

    return crud.get_authors(db, skip, limit)

@router.get("/{author_id}", response_model=schemas.Author)
def get_author(
        db: Annotated[Session, Depends(get_db)], 
        author_id: int
    ):

    db_author = crud.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author deos not exist")
    return db_author

@router.post("/{author_id}", response_model=schemas.Author)
def update_author(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Security(get_current_active_user, scopes=["super"])],
        author: schemas.AuthorUpdate, author_id: int
    ):
    
    db_author = crud.update_author(db, author_id, author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author does not exist")
    return db_author

@router.post("/{author_id}/delete", response_model=schemas.Author)
def delete_author(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Security(get_current_active_user, scopes=["super"])],
        author_id: int
    ):

    db_author = crud.delete_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author does not exist")
    return db_author