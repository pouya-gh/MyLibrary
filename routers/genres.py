from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from sql import schemas, crud

from dependencies import get_db, get_current_active_user

router = APIRouter(prefix="/genres")

@router.post("/", response_model=schemas.Genre)
def create_genre(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        genre: schemas.GenreCreate
    ):

    try:
        return crud.create_genre(db, genre)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create genre")
    
@router.get("/", response_model=list[schemas.Genre])
def get_genres(
        db: Annotated[Session, Depends(get_db)], 
        skip: int = 0, limit: int = 100
    ):

    return crud.get_genres(db, skip, limit)

@router.post("/{genre_id}", response_model=schemas.Genre)
def update_genre(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        genre: schemas.GenreUpdate, genre_id: int
    ):

    db_genre = crud.update_genre(db, genre_id, genre)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre does not exist")
    return db_genre

@router.post("/{genre_id}/delete", response_model=schemas.Genre)
def delete_genre(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        genre_id: int
    ):

    db_genre = crud.delete_genre(db, genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre does not exist")
    return db_genre