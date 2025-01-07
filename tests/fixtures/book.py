import pytest
from sqlmodel import Session

from app.api.book import Book, BookCreate, BookDataAccessLayer, Genres

@pytest.fixture(scope="session")
def books_dal(
        test_database_session: Session,
) -> BookDataAccessLayer:
    return BookDataAccessLayer(
        session=test_database_session,
    )


@pytest.fixture(scope="module")
def books(books_dal: BookDataAccessLayer) -> list[Book]:
    sample_books = [
        Book(title="Book One", author="Author A", genre=Genres.COMEDY, price=19.99, quantity=1),
        Book(title="Book Two", author="Author B", genre=Genres.HORROR, price=25.99, quantity=3),
    ]
    for book in sample_books:
        books_dal.create_book(book)
    return sample_books


@pytest.fixture(scope="module")
def create_book_request() -> BookCreate:
    return BookCreate(title="Test Book", author="Test Author", genre=Genres.FANTASY, price=12.99, quantity=3)
