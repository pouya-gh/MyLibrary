from sqlalchemy.orm import Session

from . import models, schemas

# users
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    fakehashed_passowrd = user.password + "fakehashed"
    db_user = models.User(username=user.username,
                          email = user.email,
                          hashed_password = fakehashed_passowrd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, data: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id)
    json_data = data.model_dump(exclude_none=True)
    if len(json_data) > 0:
        db_user.update(json_data)
        db.commit()
    return db_user.first()

# authors
def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(100).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def update_author(db: Session, author_id: int, data: schemas.AuthorUpdate):
    db_author = db.query(models.Author).filter(models.Author.id == author_id)
    json_data = data.model_dump(exclude_none=True)
    if len(json_data) > 0:
        db_author.update(json_data)
        db.commit()
    return db_author.first()

# genre
def get_genre_by_name(db: Session, genre_name: str):
    return db.query(models.Genre).filter(models.Genre.name == genre_name).first()

def get_genres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Genre).offset(skip).limit(limit).all()

def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.model_dump())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def update_genre(db: Session, genre_id: int, data: schemas.GenreUpdate):
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id)
    json_data = data.model_dump(exclude_none=True)
    if len(json_data) > 0:
        db_genre.update(json_data)
        db.commit()
    return db_genre.first()

# language
def get_language_by_name(db: Session, language_name: str):
    return db.query(models.Language).filter(models.Language.name == language_name).first()

def get_languages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Language).offset(skip).limit(limit).all()

def create_language(db: Session, language: schemas.LanguageCreate):
    db_language = models.Language(**language.model_dump())
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language

def update_language(db: Session, language_id: int, data: schemas.LanguageUpdate):
    db_language = db.query(models.Language).filter(models.Language.id == language_id)
    json_data = data.model_dump(exclude_none=True)
    if len(json_data) > 0:
        db_language.update(json_data)
        db.commit()
    return db_language.first()

# books
def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book_by_title(db: Session, book_title: str):
    return db.query(models.Book).filter(models.Book.title == book_title).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_books_by_genre(db: Session, 
                       genre_name: str, 
                       skip: int = 0, 
                       limit: int = 100):
    genre = get_genre_by_name(db, genre_name)
    if genre:
        return db.query(models.Book).\
            filter(models.Book.genre_id == genre.id).\
            offset(skip).limit(limit).all()
    else:
        return None

def get_books_by_language(db: Session, 
                          language_name: str, 
                          skip: int = 0, 
                          limit: int = 100):
    language = get_language_by_name(db, language_name)
    if language:
        return db.query(models.Book).\
            filter(models.Book.language_id == language.id).\
            offset(skip).limit(limit).all()
    else:
        return None
    
def filter_books_by_language_and_genre(db: Session, 
                                       language_name: str, 
                                       genre_name: str, 
                                       skip: int = 0, 
                                       limit: int = 100):
    language = get_language_by_name(db, language_name)
    genre = get_genre_by_name(db, genre_name)
    if language and genre:
        return db.query(models.Book).\
            filter(models.Book.genre_id == genre.id).\
            filter(models.Book.language_id == language.id).\
            offset(skip).limit(limit)
    else:
        return None
    
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, data: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id)
    json_data = data.model_dump(exclude_none=True)
    if len(json_data) > 0:
        db_book.update(json_data)
        db.commit()
    return db_book.first()
    
# book instances
def get_book_instance(db: Session, instance_id: str): # str id because this one is uuid
    return db.query(models.BookInstance).filter(models.BookInstance.id == instance_id).first()

def get_book_instances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BookInstance).offset(skip).limit(limit).all()

def get_book_instances_by_borrower(db: Session, 
                                   borrower_id: int, # user id
                                   skip: int = 0,
                                   limit: int = 100):
    return db.query(models.BookInstance).\
        filter(models.BookInstance.borrower_id == borrower_id).\
        offset(skip).limit(limit).all()

def create_book_instance(db: Session, book_instance: schemas.BookInstanceCreate):
    db_book_instance = models.BookInstance(**book_instance.model_dump())
    db.add(db_book_instance)
    db.commit()
    db.refresh(db_book_instance)
    return db_book_instance

def update_book_instance(db: Session, instance_id: str, data: schemas.BookInstanceUpdate):
    db_instance = db.query(models.BookInstance).filter(models.BookInstance.id == instance_id)
    json_data = data.model_dump(exclude_none=True)
    if len(json_data) > 0:
        db_instance.update(json_data)
        db.commit()
    return db_instance.first()