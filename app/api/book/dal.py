import uuid
from typing import Annotated, Sequence

from fastapi import Depends
from pydantic_core import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.db_config import get_database_session
from .exceptions import BookNotFoundException, InvalidBookDataException, BookQuantityZeroException
from .models import Book, BookCreate, BookUpdate


class BookDataAccessLayer:
    def __init__(self, session: Annotated[Session, Depends(get_database_session)]) -> None:
        self.__session = session

    def get_all_books(self) -> Sequence[Book]:
        return self.__session.exec(select(Book)).all()

    def get_book_by_id(self, book_id: uuid.UUID) -> Book:
        statement = select(Book).where(Book.book_id == book_id)
        db_book = self.__session.exec(statement).one_or_none()
        if db_book is None:
            raise BookNotFoundException(book_id=book_id)
        return db_book

    def create_book(self, book: BookCreate) -> Book:
        db_book = Book(**book.model_dump())
        try:
            self.__session.add(db_book)
            self.__session.commit()
            self.__session.refresh(db_book)
        except IntegrityError as err:
            raise InvalidBookDataException(book_id=book.book_id, error=str(err))
        return db_book

    def update_book(self, book_id: uuid.UUID, book: BookUpdate) -> Book:
        db_book = self.get_book_by_id(book_id)
        try:
            db_book.sqlmodel_update(book.model_dump(exclude_none=True))
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

    def decrement_book_quantity(self, book_id: uuid.UUID) -> Book:
        db_book = self.get_book_by_id(book_id)
        new_quantity = db_book.quantity - 1
        try:
            db_book.sqlmodel_update(BookUpdate(quantity=new_quantity).model_dump(exclude_none=True))
            self.__session.commit()
            self.__session.refresh(db_book)
        except ValidationError as err:
            raise BookQuantityZeroException(book_id=book_id, error=str(err))
        return db_book
