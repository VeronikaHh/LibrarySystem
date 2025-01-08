import uuid

import pytest

from app.api.book import (
    Book,
    BookUpdate,
    BookDataAccessLayer,
    BookNotFoundException,
    BookCreate,
    BookQuantityZeroException,
)


def test_get_all_books(books_dal: BookDataAccessLayer, books: list[Book]) -> None:
    result = books_dal.get_all_books()
    assert len(result) == len(books)
    for item in result:
        assert isinstance(item, Book)


def test_get_book_by_id(books_dal: BookDataAccessLayer, books: list[Book]) -> None:
    retrieved_book = books_dal.get_book_by_id(books[0].book_id)
    assert retrieved_book is not None
    assert isinstance(retrieved_book, Book)
    assert retrieved_book.title == books[0].title
    assert retrieved_book.author == books[0].author
    assert retrieved_book.genre == books[0].genre
    assert retrieved_book.price == books[0].price
    assert retrieved_book.quantity == books[0].quantity


def test_get_book_by_id_not_found(books_dal: BookDataAccessLayer, books: list[Book]) -> None:
    with pytest.raises(BookNotFoundException):
        books_dal.get_book_by_id(uuid.uuid4())


def test_create_book(books_dal: BookDataAccessLayer, create_book_request: BookCreate) -> None:
    created_book = books_dal.create_book(book=create_book_request)
    assert created_book is not None
    assert created_book.title == create_book_request.title
    assert created_book.author == create_book_request.author


def test_update_book(books_dal: BookDataAccessLayer, books: list[Book]) -> None:
    updated_book = books_dal.update_book(book_id=books[0].book_id, book=BookUpdate(title="Updated title"))
    assert updated_book.title == "Updated title"


def test_check_available(books_dal: BookDataAccessLayer, book_available: Book) -> None:
    books_dal.check_available(book_available.book_id)


def test_check_available_exception(books_dal: BookDataAccessLayer, book_unavailable: Book) -> None:
    with pytest.raises(BookQuantityZeroException):
        books_dal.check_available(book_unavailable.book_id)


def test_increment_book_quantity(books_dal: BookDataAccessLayer, book_available: Book) -> None:
    updated_book = books_dal.increment_book_quantity(book_available.book_id)
    assert updated_book.quantity == book_available.quantity + 1


def test_decrement_book_quantity(books_dal: BookDataAccessLayer, book_available: Book) -> None:
    updated_book = books_dal.decrement_book_quantity(book_available.book_id)
    assert updated_book.quantity == book_available.quantity - 1


def test_delete_book(books_dal: BookDataAccessLayer, book_available: Book) -> None:
    books_dal.delete_book(book_id=book_available.book_id)
    with pytest.raises(BookNotFoundException):
        books_dal.get_book_by_id(book_available.book_id)
