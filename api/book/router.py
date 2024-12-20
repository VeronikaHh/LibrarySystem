import uuid
from http.client import HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db_config import get_database_session
from .models import Book, BookUpdate

router = APIRouter(prefix="/books",tags=["Book"])


@router.get("", status_code=200)
async def get_books(session: Annotated[Session, Depends(get_database_session)]):
    books = session.exec(select(Book)).all()
    return books

@router.get("/{book_id}", status_code=200)
async def get_book_by_id(book_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    book = session.get(Book, book_id)
    if book is None:
        raise HTTPException()
    return book

@router.post("", status_code=201)
async def create_book(book: Book, session: Annotated[Session, Depends(get_database_session)]):
    db_book = Book(**book.model_dump())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.put("/{book_id}", status_code=201)
async def update_book(book_id: uuid.UUID, book: BookUpdate, session: Annotated[Session, Depends(get_database_session)]):
    db_book = session.get(Book, book_id)
    if db_book is None:
        raise HTTPException()
    db_book.sqlmodel_update(book.model_dump())
    session.commit()
    session.refresh(db_book)
    return db_book

@router.delete("/{book_id}", status_code=200)
async def delete_book(book_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException()
    session.delete(book)
    session.commit()
    return {"ok": True}