from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from sql import crud, models, schemas
from sql.database import SessionLocal, engine
from dependencies import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def index():
    return {"msg": "Welcome!"}

# users
@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User email/username already exists")

@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user

@app.post("/users/{user_id}", response_model=schemas.User)
def update_user(data: schemas.UserUpdate, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user

@app.post("/users/{user_id}/delete", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_user

# authors
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_author(db, author)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create author")
    
@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip, limit)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author deos not exist")
    return db_author

@app.post("/authors/{author_id}", response_model=schemas.Author)
def update_author(author: schemas.AuthorUpdate, author_id: int, db: Session = Depends(get_db)):
    db_author = crud.update_author(db, author_id, author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author does not exist")
    return db_author

@app.post("/authors/{author_id}/delete", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.delete_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author does not exist")
    return db_author

# genre
@app.post("/genres/", response_model=schemas.Genre)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_genre(db, genre)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create genre")
    
@app.get("/genres/", response_model=list[schemas.Genre])
def get_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_genres(db, skip, limit)

@app.post("/genres/{genre_id}", response_model=schemas.Genre)
def update_genre(genre: schemas.GenreUpdate, genre_id: int, db: Session = Depends(get_db)):
    db_genre = crud.update_genre(db, genre_id, genre)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre does not exist")
    return db_genre

@app.post("/genres/{genre_id}/delete", response_model=schemas.Genre)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    db_genre = crud.delete_genre(db, genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre does not exist")
    return db_genre

# language
@app.post("/languages/", response_model=schemas.Language)
def create_language(language: schemas.LanguageCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_language(db, language)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create language")
    
@app.get("/languages/", response_model=list[schemas.Language])
def get_languages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_languages(db, skip, limit)

@app.post("/languages/{language_id}", response_model=schemas.Language)
def update_language(language: schemas.LanguageUpdate, language_id: int, db: Session = Depends(get_db)):
    db_language = crud.update_language(db, language_id, language)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language does not exist")
    return db_language

@app.post("/languages/{language_id}/delete", response_model=schemas.Language)
def delete_language(language_id: int, db: Session = Depends(get_db)):
    db_language = crud.delete_language(db, language_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language does not exist")
    return db_language

# book
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_book(db, book)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create book")
    
@app.get("/books/", response_model=list[schemas.Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip, limit)

@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book deos not exist")
    return db_book

@app.post("/books/{book_id}", response_model=schemas.Book)
def update_book(book: schemas.BookUpdate, book_id: int, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id, book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book does not exist")
    return db_book

@app.post("/books/{book_id}/delete", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book does not exist")
    return db_book

# book instance
@app.post("/bookinstances/", response_model=schemas.BookInstance)
def create_bookinstance(instance: schemas.BookInstanceCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_book_instance(db, instance)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Failed to create book instance")
    
@app.get("/bookinstances/", response_model=list[schemas.BookInstance])
def get_bookinstances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_book_instances(db, skip, limit)

@app.get("/bookinstances/{instance_id}", response_model=schemas.BookInstance)
def get_bookinstance(instance_id: str, db: Session = Depends(get_db)):
    db_bookinstance = crud.get_book_instance(db, instance_id)
    if db_bookinstance is None:
        raise HTTPException(status_code=404, detail="Book instance deos not exist")
    return db_bookinstance

@app.post("/bookinstances/{instance_id}", response_model=schemas.BookInstance)
def update_bookinstance(instance: schemas.BookInstanceUpdate, instance_id: str, db: Session = Depends(get_db)):
    db_bookinstance = crud.update_book_instance(db, instance_id, crud)
    if db_bookinstance is None:
        raise HTTPException(status_code=404, detail="Book instance does not exist")
    return db_bookinstance

@app.post("/bookinstances/{instance_id}/delete", response_model=schemas.BookInstance)
def delete_bookinstance(instance_id: str, db: Session = Depends(get_db)):
    db_bookinstance = crud.delete_book_instance(db, instance_id)
    if db_bookinstance is None:
        raise HTTPException(status_code=404, detail="Book does not exist")
    return db_bookinstance