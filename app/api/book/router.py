import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status

from .models import BookCreate, BookUpdate, Book
from .service import BookService

router = APIRouter(prefix="/books", tags=["Book"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_books(book_service: Annotated[BookService, Depends()]) -> list[Book]:
    return list(book_service.get_all_books())


@router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: uuid.UUID, book_service: Annotated[BookService, Depends()]) -> Book:
    return book_service.get_book_by_id(book_id=book_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, book_service: Annotated[BookService, Depends()]) -> Book:
    return book_service.create_book(book=book)


@router.put("/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(
        book_id: uuid.UUID,
        book: BookUpdate,
        book_service: Annotated[BookService, Depends()],
) -> Book:
    return book_service.update_book(book_id=book_id, book=book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: uuid.UUID, book_service: Annotated[BookService, Depends()]) -> None:
    return book_service.delete_book(book_id=book_id)
