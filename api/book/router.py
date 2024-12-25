import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status

from .dal import BookDataAccessLayer
from .models import BookCreateUpdate, Book

router = APIRouter(prefix="/books", tags=["Book"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_books(book_dal: Annotated[BookDataAccessLayer, Depends()]) -> list[Book]:
    return list(book_dal.get_all_books())


@router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: uuid.UUID, book_dal: Annotated[BookDataAccessLayer, Depends()]) -> Book:
    return book_dal.get_book_by_id(book_id=book_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreateUpdate, book_dal: Annotated[BookDataAccessLayer, Depends()]) -> Book:
    return book_dal.create_book(book=book)


@router.put("/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(
        book_id: uuid.UUID,
        book: BookCreateUpdate,
        book_dal: Annotated[BookDataAccessLayer, Depends()],
) -> Book:
    return book_dal.update_book(book_id=book_id, book=book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: uuid.UUID, book_dal: Annotated[BookDataAccessLayer, Depends()]) -> None:
    return book_dal.delete_book(book_id=book_id)
