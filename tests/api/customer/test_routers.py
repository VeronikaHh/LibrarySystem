import uuid

from fastapi.testclient import TestClient

from app.api.customer import Customer, CustomerCreate


def test_get_all_customers(test_client: TestClient) -> None:
    response = test_client.get("/customers")
    assert response.status_code == 200


def test_get_customer_by_id(test_client: TestClient, customers: list[Customer]) -> None:
    customer_id = customers[0].customer_id
    response = test_client.get(f"/customers/{customer_id}")
    assert response.status_code == 200


def test_get_customer_by_id_not_exist(test_client: TestClient) -> None:
    customer_id = uuid.uuid4()
    response = test_client.get(f"/customers/{customer_id}")
    assert response.status_code == 404


def test_create_customer(test_client: TestClient, create_customer_request: CustomerCreate) -> None:
    response = test_client.post("/customers", json=create_customer_request.model_dump())
    assert response.status_code == 201


def test_update_customer(test_client: TestClient, customers: list[Customer]) -> None:
    customer_id = customers[0].customer_id
    response = test_client.put(f"/customers/{customer_id}", json={})
    assert response.status_code == 200


def test_update_customer_not_exist(test_client: TestClient) -> None:
    customer_id = uuid.uuid4()
    response = test_client.put(f"/customers/{customer_id}", json={})
    assert response.status_code == 404


def test_delete_customer(test_client: TestClient, customers: list[Customer]) -> None:
    customer_id = customers[0].customer_id
    response = test_client.delete(f"/customers/{customer_id}")
    assert response.status_code == 204


def test_delete_customer_not_exist(test_client: TestClient) -> None:
    customer_id = uuid.uuid4()
    response = test_client.delete(f"/customers/{customer_id}")
    assert response.status_code == 404
