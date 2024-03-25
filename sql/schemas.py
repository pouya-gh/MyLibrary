from pydantic import BaseModel
from sql.models import BookInstanceStatus

import datetime
import uuid

# book instance
class BookInstanceBase(BaseModel):
    imprint: str
    due_back: datetime.date
    status: BookInstanceStatus
    borrower_id: int
    book_id: int

class BookInstanceCreate(BookInstanceBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "imprint": "Foo",
                    "due_back": None,
                    "status": "Available",
                    "borrower_id": 0,
                    "book_id": 3
                }
            ]
        }
    }

class BookInstanceUpdate(BaseModel):
    """
    Same fields as BookInstanceCreate model. But all these fields can
    be empty, which means you don't want them to be updated.
    """
    imprint: str | None = None
    due_back: datetime.date | None = None
    status: BookInstanceStatus | None = None
    borrower_id: int | None = None
    book_id: int | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "Maintenance",
                    "borrower_id": 0
                }
            ]
        }
    }

class BookInstance(BookInstanceBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "imprint": "Foo",
                    "due_back": datetime.date.today(),
                    "status": "On loan",
                    "borrower_id": 5,
                    "book_id": 3,
                    'id': uuid.uuid4(),
                }
            ]
        }

# book
class BookBase(BaseModel):
    title: str
    description: str
    author_id: int
    genre_id: int
    language_id: int

class BookCreate(BookBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Foo",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                    "author_id": 3,
                    "genre_id": 9,
                    "language_id": 1
                }
            ]
        }
    }

class BookUpdate(BaseModel):
    """
    Same fields as BookCreate model. But all these fields can
    be empty, which means you don't want them to be updated.
    """
    title: str | None = None
    description: str | None = None
    author_id: int | None = None
    genre_id: int | None = None
    language_id: int | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Foobar",
                    "description": "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
                    "genre_id": 8,
                }
            ]
        }
    }

class Book(BookBase):
    id: int
    instances: list[BookInstance] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "imprint": "Foo",
                    "due_back": datetime.date.today(),
                    "status": "On loan",
                    "borrower_id": 5,
                    "book_id": 3,
                    "id": 2,
                    "instances": []
                }
            ]
        }

# genre
class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Thriller",
                }
            ]
        }
    } 

class GenreUpdate(BaseModel):
    name: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Fantasy",
                }
            ]
        }
    } 

class Genre(GenreBase):
    id: int
    books: list[Book] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "name": "Fantasy",
                    "books": [],
                }
            ]
        }

# language
class LanguageBase(BaseModel):
    name: str

class LanguageCreate(GenreBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "French",
                }
            ]
        }
    }  

class LanguageUpdate(BaseModel):
    name: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "German",
                }
            ]
        }
    }  

class Language(GenreBase):
    id: int
    books: list[Book] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "name": "Farsi",
                    "books": [],
                }
            ]
        }

# author
class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: datetime.date
    date_of_death: datetime.date | None
    
class AuthorCreate(AuthorBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Foo",
                    "last_name": "Barsson",
                    "date_of_birth": datetime.date.today() - datetime.timedelta(weeks=2650),
                    "date_of_death": None,
                }
            ]
        }
    }

class AuthorUpdate(BaseModel):
    """
    Same fields as AuthorCreate model. But all these fields can
    be empty, which means you don't want them to be updated.
    """
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime.date | None = None
    date_of_death: datetime.date | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "date_of_death": datetime.date.today(),
                }
            ]
        }
    }

class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "first_name": "Foo",
                    "last_name": "Barsson",
                    "date_of_birth": datetime.date.today() - datetime.timedelta(weeks=2650),
                    "date_of_death": datetime.date.today() - datetime.timedelta(weeks=500),
                    "books": []
                }
            ]
        }

# user
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "foobar",
                    "email": "foo@bar.com",
                    "password": "a_very@good&pssword1",
                }
            ]
        }
    }

class UserUpdate(BaseModel):
    """
    Same fields as AuthorCreate model minus the password field. 
    But all these fields can be empty, which means you don't 
    want them to be updated.
    """
    username: str | None = None
    email: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "foo@gmail.com",
                }
            ]
        }
    }

class UserSelfUpdate(BaseModel):
    """
    Same fields as UserUpdate model minus the is_superuser field. 
    But all these fields can be empty, which means you don't 
    want them to be updated.
    """
    username: str | None = None
    email: str | None = None
    is_active: bool | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "foo@gmail.com",
                }
            ]
        }
    }

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    borrowed_book_instances: list[BookInstance] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "username": "foobar",
                    "email": "foo@bar.com",
                    "is_active": True,
                    "borrowed_book_instances": [],
                }
            ]
        }