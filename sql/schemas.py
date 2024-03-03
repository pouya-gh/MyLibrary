from pydantic import BaseModel
from sql.models import BookInstanceStatus

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

class BookInstanceUpdate(BaseModel):
    imprint: str | None = None
    due_back: datetime.date | None = None
    status: BookInstanceStatus | None = None
    borrower_id: int | None = None
    book_id: int | None = None

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

class BookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    author_id: int | None = None
    genre_id: int | None = None
    language_id: int | None = None

class Book(BookBase):
    id: int
    instances: list[BookInstance] = []

    class Config:
        orm_mode = True

# genre
class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass 

class GenreUpdate(BaseModel):
    name: str | None = None

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

class LanguageUpdate(BaseModel):
    name: str | None = None

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

class AuthorUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime.date | None = None
    date_of_death: datetime.date | None = None

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

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None

class User(UserBase):
    id: int
    is_active: bool
    borrowed_book_instances: list[BookInstance] = []

    class Config:
        orm_mode = True