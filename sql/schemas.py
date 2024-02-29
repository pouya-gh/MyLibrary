from pydantic import BaseModel
from models import BookInstanceStatus

import datetime

# book instance
class BookInstanceBase(BaseModel):
    imprint: str
    due_back: datetime.date
    status: BookInstanceStatus
    borrower_id: int
    book_id: int

class BookInstanceCreate(BookInstanceBase):
    pass

class BookInstance(BookInstanceBase):
    id: str

    class Config:
        orm_mode = True

# book
class BookBase(BaseModel):
    title: str
    description: str
    author_id: int
    genre_id: int
    language_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    instances: list[BookInstance] = []

    class Config:
        orm_mode = True

# genre
class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass 

class Genre(GenreBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True

# language
class LanguageBase(BaseModel):
    name: str

class LanguageCreate(GenreBase):
    pass 

class Language(GenreBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True

# author
class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: datetime.date
    date_of_death: datetime.date
    
class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True

# user
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    borrowed_book_instances: list[BookInstance] = []

    class Config:
        orm_mode = True