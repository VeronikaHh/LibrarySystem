import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from db_config import get_database_session
from .exceptions import BookNotFoundError, InvalidBookDataError
from .models import Book, BookCreateUpdate

router = APIRouter(prefix="/books", tags=["Book"])


@router.get("", status_code=200)
async def get_books(session: Annotated[Session, Depends(get_database_session)]):
    db_books = session.exec(select(Book)).all()
    return db_books


@router.get("/{book_id}", status_code=200)
async def get_book_by_id(book_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    db_book = session.get(Book, book_id)
    if db_book is None:
        raise BookNotFoundError(book_id=book_id)
    return db_book


@router.post("", status_code=201)
async def create_book(book: BookCreateUpdate, session: Annotated[Session, Depends(get_database_session)]):
    db_book = Book(**book.model_dump())
    try:
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
    except IntegrityError as err:
        raise InvalidBookDataError(book_id=book.book_id, error=str(err))
    return db_book


@router.put("/{book_id}", status_code=201)
async def update_book(book_id: uuid.UUID, book: BookCreateUpdate, session: Annotated[Session, Depends(get_database_session)]):
    db_book = session.get(Book, book_id)
    if db_book is None:
        raise BookNotFoundError(book_id=book_id)
    try:
        db_book.sqlmodel_update(book.model_dump())
        session.commit()
        session.refresh(db_book)
    except IntegrityError as err:
        raise InvalidBookDataError(book_id=book.book_id, error=str(err))
    return db_book


@router.delete("/{book_id}", status_code=200)
async def delete_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    db_book = session.get(Book, book_id)
    if db_book is None:
        raise BookNotFoundError(book_id=book_id)
    session.delete(db_book)
    session.commit()
    return {"ok": True}
