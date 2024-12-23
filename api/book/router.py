import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from db_config import get_database_session
from .exceptions import BookNotFoundException, InvalidBookDataException
from .models import Book, BookCreateUpdate

router = APIRouter(prefix="/books", tags=["Book"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_books(session: Annotated[Session, Depends(get_database_session)]):
    db_books = session.exec(select(Book)).all()
    return db_books


@router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    db_book = session.get(Book, book_id)
    if db_book is None:
        raise BookNotFoundException(book_id=book_id)
    return db_book


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreateUpdate, session: Annotated[Session, Depends(get_database_session)]):
    db_book = Book(**book.model_dump())
    try:
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
    except IntegrityError as err:
        raise InvalidBookDataException(book_id=book.book_id, error=str(err))
    return db_book


@router.put("/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(book_id: uuid.UUID, book: BookCreateUpdate, session: Annotated[Session, Depends(get_database_session)]):
    db_book = session.get(Book, book_id)
    if db_book is None:
        raise BookNotFoundException(book_id=book_id)
    try:
        db_book.sqlmodel_update(book.model_dump())
        session.commit()
        session.refresh(db_book)
    except IntegrityError as err:
        raise InvalidBookDataException(book_id=book.book_id, error=str(err))
    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    db_book = session.get(Book, book_id)
    if db_book is None:
        raise BookNotFoundException(book_id=book_id)
    session.delete(db_book)
    session.commit()
    return {"ok": True}
