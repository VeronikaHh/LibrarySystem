import uuid

from fastapi.testclient import TestClient

from app.api.book import Book, BookCreate


def test_get_all_books(test_client: TestClient) -> None:
    response = test_client.get("/books")
    assert response.status_code == 200


def test_get_book_by_id(test_client: TestClient, books: list[Book]) -> None:
    book_id = books[0].book_id
    response = test_client.get(f"/books/{book_id}")
    assert response.status_code == 200


def test_get_book_by_id_not_exist(test_client: TestClient) -> None:
    book_id = uuid.uuid4()
    response = test_client.get(f"/books/{book_id}")
    assert response.status_code == 404


def test_create_book(test_client: TestClient, create_book_request: BookCreate) -> None:
    response = test_client.post("/books", json=create_book_request.model_dump())
    assert response.status_code == 201


def test_update_book(test_client: TestClient, books: list[Book]) -> None:
    book_id = books[0].book_id
    response = test_client.put(f"/books/{book_id}", json={})
    assert response.status_code == 200


def test_update_book_id_not_exist(test_client: TestClient) -> None:
    book_id = uuid.uuid4()
    response = test_client.put(f"/books/{book_id}", json={})
    assert response.status_code == 404


def test_delete_book(test_client: TestClient, books: list[Book]) -> None:
    book_id = books[0].book_id
    response = test_client.delete(f"/books/{book_id}")
    assert response.status_code == 204


def test_delete_book_id_not_exist(test_client: TestClient) -> None:
    book_id = uuid.uuid4()
    response = test_client.delete(f"/books/{book_id}")
    assert response.status_code == 404
