import uuid
from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.db_config import get_database_session
from .exceptions import BookNotFoundException, InvalidBookDataException
from .models import Book, BookCreateUpdate


class BookDataAccessLayer:
    def __init__(self, session: Annotated[Session, Depends(get_database_session)]):
        self.__session = session

    def get_all_books(self) -> Sequence[Book]:
        db_books = self.__session.exec(select(Book)).all()
        return db_books

    def get_book_by_id(self, book_id: uuid.UUID) -> Book:
        statement = select(Book).where(Book.book_id == book_id)
        db_book = self.__session.exec(statement).one_or_none()
        if db_book is None:
            raise BookNotFoundException(book_id=book_id)
        return db_book

    def create_book(self, book: BookCreateUpdate) -> Book:
        db_book = Book(**book.model_dump())
        try:
            self.__session.add(db_book)
            self.__session.commit()
            self.__session.refresh(db_book)
        except IntegrityError as err:
            raise InvalidBookDataException(book_id=book.book_id, error=str(err))
        return db_book

    def update_book(self, book_id: uuid.UUID, book: BookCreateUpdate) -> Book:
        db_book = self.get_book_by_id(book_id)
        try:
            db_book.sqlmodel_update(book.model_dump())
            self.__session.commit()
            self.__session.refresh(db_book)
        except IntegrityError as err:
            raise InvalidBookDataException(book_id=book_id, error=str(err))
        return db_book

    def delete_book(self, book_id: uuid.UUID) -> None:
        db_book = self.get_book_by_id(book_id)
        try:
            self.__session.delete(db_book)
            self.__session.commit()
        except IntegrityError as err:
            raise InvalidBookDataException(book_id=book_id, error=str(err))
        return None
