import uuid

import pytest

from app.api.order import (
    Order,
    OrderUpdate,
    OrderService,
    OrderNotFoundException,
    OrderCreate,
)


def test_get_all_orders(orders_service: OrderService, orders: list[Order]) -> None:
    result = orders_service.get_all_orders()
    assert len(result) == len(orders)
    for item in result:
        assert isinstance(item, Order)


def test_get_order_by_id(orders_service: OrderService, orders: list[Order]) -> None:
    retrieved_order = orders_service.get_order_by_id(orders[0].order_id)
    assert retrieved_order is not None
    assert isinstance(retrieved_order, Order)
    assert retrieved_order.book_id == orders[0].book_id
    assert retrieved_order.customer_id == orders[0].customer_id
    assert retrieved_order.employee_id == orders[0].employee_id


def test_get_order_by_id_not_found(orders_service: OrderService, orders: list[Order]) -> None:
    with pytest.raises(OrderNotFoundException):
        orders_service.get_order_by_id(uuid.uuid4())


def test_create_order(orders_service: OrderService, create_order_request: OrderCreate) -> None:
    created_order = orders_service.create_order(order=create_order_request)
    assert created_order is not None
    assert created_order.book_id == create_order_request.book_id
    assert created_order.customer_id == create_order_request.customer_id


def test_update_order(orders_service: OrderService, orders: list[Order]) -> None:
    updated_order = orders_service.update_order(
        order_id=orders[0].order_id,
        order=OrderUpdate(is_returned=True),
    )
    assert updated_order.is_returned


def test_delete_order(orders_service: OrderService, orders: list[Order]) -> None:
    orders_service.delete_order(order_id=orders[0].order_id)
    with pytest.raises(OrderNotFoundException):
        orders_service.get_order_by_id(orders[0].order_id)


def test_close_order(orders_service: OrderService, order: Order) -> None:
    closed_order = orders_service.close_order(order_id=order.order_id)
    assert closed_order.is_returned == True
