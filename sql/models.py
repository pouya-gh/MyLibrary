from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid, Date, Text, Enum
from sqlalchemy.orm import relationship

import uuid
import enum

from .database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(length=100), unique=True, index=True, nullable=False)
    email = Column(String(length=150), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    borrowed_book_instances = relationship("BookInstance", back_populates='borrower')

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(length=100), nullable=False)
    last_name = Column(String(length=100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    date_of_death = Column(Date, nullable=True)

    books = relationship("Book", back_populates='author', cascade='all, delete, save-update')

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), unique=True, index=True, nullable=False)

    books = relationship('Book', back_populates='genre')

class Language(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), unique=True, index=True, nullable=False)

    books = relationship('Book', back_populates='language')

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=100), unique=True, index=True, nullable=False)
    description = Column(Text)
    author_id = Column(Integer, ForeignKey('authors.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    language_id = Column(Integer, ForeignKey('languages.id'))

    author = relationship("Author", back_populates='books')
    genre = relationship('Genre', back_populates='books')
    language = relationship('Language', back_populates='books')

    instances = relationship('BookInstance', back_populates='book', cascade='all, delete, save-update')

class BookInstanceStatus(enum.Enum):
    m = 'Maintenance'
    o = 'On loan'
    a = 'Available'
    r = 'Reserved'

class BookInstance(Base):
    __tablename__ = 'bookinstances'

    id = Column(Uuid(as_uuid=False), primary_key=True, default=uuid.uuid4)
    book_id = Column(Integer, ForeignKey('books.id'))
    imprint = Column(String)
    due_back = Column(Date, nullable=True, index=True)
    borrower_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Enum(BookInstanceStatus), default='m')

    book = relationship('Book', back_populates='instances')
    borrower = relationship('User', back_populates='borrowed_book_instances')