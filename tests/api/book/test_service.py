import uuid

import pytest

from app.api.book import (
    Book,
    BookUpdate,
    BookService,
    BookNotFoundException,
    BookCreate,
    BookQuantityZeroException,
)


def test_get_all_books(books_service: BookService, books: list[Book]) -> None:
    result = books_service.get_all_books()
    assert len(result) == len(books)
    for item in result:
        assert isinstance(item, Book)


def test_get_book_by_id(books_service: BookService, books: list[Book]) -> None:
    retrieved_book = books_service.get_book_by_id(books[0].book_id)
    assert retrieved_book is not None
    assert isinstance(retrieved_book, Book)
    assert retrieved_book.title == books[0].title
    assert retrieved_book.author == books[0].author
    assert retrieved_book.genre == books[0].genre
    assert retrieved_book.price == books[0].price
    assert retrieved_book.quantity == books[0].quantity


def test_get_book_by_id_not_found(books_service: BookService, books: list[Book]) -> None:
    with pytest.raises(BookNotFoundException):
        books_service.get_book_by_id(uuid.uuid4())


def test_create_book(books_service: BookService, create_book_request: BookCreate) -> None:
    created_book = books_service.create_book(book=create_book_request)
    assert created_book is not None
    assert created_book.title == create_book_request.title
    assert created_book.author == create_book_request.author


def test_update_book(books_service: BookService, books: list[Book]) -> None:
    updated_book = books_service.update_book(book_id=books[0].book_id, book=BookUpdate(title="Updated title"))
    assert updated_book.title == "Updated title"


def test_check_available(books_service: BookService, book_available: Book) -> None:
    books_service.check_available(book_available.book_id)


def test_check_available_exception(books_service: BookService, book_unavailable: Book) -> None:
    with pytest.raises(BookQuantityZeroException):
        books_service.check_available(book_unavailable.book_id)


def test_increment_book_quantity(books_service: BookService, book_available: Book) -> None:
    updated_book = books_service.increment_book_quantity(book_available.book_id)
    assert updated_book.quantity == book_available.quantity + 1


def test_decrement_book_quantity(books_service: BookService, book_available: Book) -> None:
    updated_book = books_service.decrement_book_quantity(book_available.book_id)
    assert updated_book.quantity == book_available.quantity - 1


def test_delete_book(books_service: BookService, book_without_orders: Book) -> None:
    books_service.delete_book(book_id=book_without_orders.book_id)
    with pytest.raises(BookNotFoundException):
        books_service.get_book_by_id(book_without_orders.book_id)
