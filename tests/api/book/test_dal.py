from app.api.book import Book, BookCreateUpdate, BookDataAccessLayer

def test_get_all_books(books_dal: BookDataAccessLayer, books: list[Book]) -> None:
    result = books_dal.get_all_books()
    assert len(result) == 2
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


def test_create_book(books_dal: BookDataAccessLayer, create_book_request: Book) -> None:
    created_book = books_dal.create_book(book=create_book_request)
    assert created_book is not None
    assert created_book.title == create_book_request.title
    assert created_book.author == create_book_request.author


def test_update_book(books_dal: BookDataAccessLayer, books: list[Book]):
    updated_book = books_dal.update_book(book_id=books[0].book_id, book=BookCreateUpdate(title="Updated title"))
    assert updated_book.title == "Updated title"

def test_delete_book(books_dal: BookDataAccessLayer, books: list[Book]) -> None:
    pass
