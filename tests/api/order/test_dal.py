import uuid

import pytest

from app.api.order import (
    Order,
    OrderUpdate,
    OrderDataAccessLayer,
    OrderNotFoundException,
    OrderCreate,
)


def test_get_all_orders(orders_dal: OrderDataAccessLayer, orders: list[Order]) -> None:
    result = orders_dal.get_all_orders()
    assert len(result) == len(orders)
    for item in result:
        assert isinstance(item, Order)


def test_get_order_by_id(orders_dal: OrderDataAccessLayer, orders: list[Order]) -> None:
    retrieved_order = orders_dal.get_order_by_id(orders[0].order_id)
    assert retrieved_order is not None
    assert isinstance(retrieved_order, Order)
    assert retrieved_order.book_id == orders[0].book_id
    assert retrieved_order.customer_id == orders[0].customer_id
    assert retrieved_order.employee_id == orders[0].employee_id


def test_get_order_by_id_not_found(orders_dal: OrderDataAccessLayer, orders: list[Order]) -> None:
    with pytest.raises(OrderNotFoundException):
        orders_dal.get_order_by_id(uuid.uuid4())


def test_create_order(orders_dal: OrderDataAccessLayer, create_order_request: OrderCreate) -> None:
    created_order = orders_dal.create_order(order=create_order_request)
    assert created_order is not None
    assert created_order.book_id == create_order_request.book_id
    assert created_order.customer_id == create_order_request.customer_id


def test_update_order(orders_dal: OrderDataAccessLayer, orders: list[Order]) -> None:
    updated_order = orders_dal.update_order(
        order_id=orders[0].order_id,
        order=OrderUpdate(is_returned=True),
    )
    assert updated_order.is_returned


def test_delete_order(orders_dal: OrderDataAccessLayer, orders: list[Order]) -> None:
    orders_dal.delete_order(order_id=orders[0].order_id)
    with pytest.raises(OrderNotFoundException):
        orders_dal.get_order_by_id(orders[0].order_id)


def test_close_order(orders_dal: OrderDataAccessLayer, order: Order) -> None:
    closed_order = orders_dal.close_order(order_id=order.order_id)
    assert closed_order.is_returned == True

# def test_get_orders_for_customer(orders_dal: OrderDataAccessLayer, orders: list[Order]) -> None:
#     # Test getting all orders for a customer
#     customer_id = orders[0].customer_id
#     all_orders = orders_dal.get_orders_for_customer(customer_id)
#     assert len(all_orders) == len([order for order in orders if order.customer_id == customer_id])
#
#     # Test getting only non-returned orders for a customer
#     non_returned_orders = orders_dal.get_orders_for_customer(customer_id, returned=False)
#     assert len(non_returned_orders) == len(
#         [order for order in orders if order.customer_id == customer_id and not order.is_returned])
#
#     # Test getting only returned orders for a customer
#     returned_orders = orders_dal.get_orders_for_customer(customer_id, returned=True)
#     assert len(returned_orders) == len(
#         [order for order in orders if order.customer_id == customer_id and order.is_returned])
#
#     # Test handling a non-existent customer
#     non_existent_customer_id = uuid.uuid4()
#     with pytest.raises(CustomerNotFoundException):
#         orders_dal.get_orders_for_customer(non_existent_customer_id)
