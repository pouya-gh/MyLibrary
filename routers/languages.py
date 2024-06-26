from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from sql import schemas, crud

from dependencies import get_db, get_current_active_user

router = APIRouter(prefix="/languages")

@router.post("/", response_model=schemas.Language, tags=["admin"])
def create_language(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Security(get_current_active_user, scopes=["super"])],
        language: schemas.LanguageCreate
    ):

    try:
        return crud.create_language(db, language)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create language")
    
@router.get("/", response_model=list[schemas.LanguageInline], tags=["languages"])
def get_languages(
        db: Annotated[Session, Depends(get_db)], 
        skip: int = 0, limit: int = 100
    ):

    return crud.get_languages(db, skip, limit)

@router.patch("/{language_id}", response_model=schemas.Language, tags=["admin"])
def update_language(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Security(get_current_active_user, scopes=["super"])],
        language: schemas.LanguageUpdate, language_id: int
    ):

    db_language = crud.update_language(db, language_id, language)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language does not exist")
    return db_language

@router.delete("/{language_id}/delete", response_model=schemas.Language, tags=["admin"])
def delete_language(
        db: Annotated[Session, Depends(get_db)], 
        current_user: Annotated[schemas.User, Security(get_current_active_user, scopes=["super"])],
        language_id: int
    ):

    db_language = crud.delete_language(db, language_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language does not exist")
    return db_language
