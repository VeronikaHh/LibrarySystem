import uuid

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

from app.api.order import Order, OrderCreate


def test_get_all_orders(test_client: TestClient) -> None:
    response = test_client.get("/orders")
    assert response.status_code == 200


def test_get_order_by_id(test_client: TestClient, orders: list[Order]) -> None:
    order_id = orders[0].order_id
    response = test_client.get(f"/orders/{order_id}")
    assert response.status_code == 200


def test_get_order_by_id_not_exist(test_client: TestClient) -> None:
    order_id = uuid.uuid4()
    response = test_client.get(f"/orders/{order_id}")
    assert response.status_code == 404


def test_create_order(test_client: TestClient, create_order_request: OrderCreate) -> None:
    response = test_client.post("/orders", json=jsonable_encoder(create_order_request))
    assert response.status_code == 201


def test_update_order(test_client: TestClient, orders: list[Order]) -> None:
    order_id = orders[0].order_id
    response = test_client.put(f"/orders/{order_id}", json={})
    assert response.status_code == 200


def test_update_order_not_exist(test_client: TestClient) -> None:
    order_id = uuid.uuid4()
    response = test_client.put(f"/orders/{order_id}", json={})
    assert response.status_code == 404


def test_delete_order(test_client: TestClient, orders: list[Order]) -> None:
    order_id = orders[0].order_id
    response = test_client.delete(f"/orders/{order_id}")
    assert response.status_code == 204


def test_delete_order_not_exist(test_client: TestClient) -> None:
    order_id = uuid.uuid4()
    response = test_client.delete(f"/orders/{order_id}")
    assert response.status_code == 404

def test_close_order(test_client: TestClient, order: Order) -> None:
    order_id = order.order_id
    response = test_client.patch(f"/orders/{order_id}/close", json={})
    assert response.status_code == 200
