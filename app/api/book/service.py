import uuid
from typing import Annotated

from fastapi import Depends

from .dal import BookDataAccessLayer
from .exceptions import BookQuantityZeroException
from .models import Book, BookUpdate, BookCreate


class BookService:
    def __init__(
            self,
            books_dal: Annotated[BookDataAccessLayer, Depends()],
    ) -> None:
        self.books_dal = books_dal

    def get_all_books(self) -> list[Book]:
        return list(self.books_dal.get_all_books())

    def get_book_by_id(self, book_id: uuid.UUID) -> Book:
        return self.books_dal.get_book_by_id(book_id)

    def create_book(self, book: BookCreate) -> Book:
        return self.books_dal.create_book(book)

    def update_book(self, book_id: uuid.UUID, book: BookUpdate) -> Book:
        return self.books_dal.update_book(book_id, book)

    def delete_book(self, book_id: uuid.UUID) -> None:
        return self.books_dal.delete_book(book_id)

    def update_book_quantity(self, book_id: uuid.UUID, delta: int) -> Book:
        book = self.books_dal.get_book_by_id(book_id)
        new_quantity = book.quantity + delta
        return self.books_dal.update_book(book_id, BookUpdate(quantity=new_quantity))

    def increment_book_quantity(self, book_id: uuid.UUID) -> Book:
        return self.update_book_quantity(book_id, 1)

    def decrement_book_quantity(self, book_id: uuid.UUID) -> Book:
        return self.update_book_quantity(book_id, -1)

    def check_available(self, book_id: uuid.UUID) -> None:
        requested_book = self.get_book_by_id(book_id)
        if not requested_book.quantity:
            raise BookQuantityZeroException(book_id=book_id)
