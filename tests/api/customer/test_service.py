import uuid

import pytest

from app.api.customer import (
    Customer,
    CustomerUpdate,
    CustomerService,
    CustomerNotFoundException,
    CustomerCreate,
    CustomerIsOwerException,
    CustomerReachedOrderLimitException,
)


def test_get_all_customers(customers_service: CustomerService, customers: list[Customer]) -> None:
    result = customers_service.get_all_customers()
    assert len(result) == len(customers)
    for item in result:
        assert isinstance(item, Customer)


def test_get_customer_by_id(customers_service: CustomerService, customers: list[Customer]) -> None:
    retrieved_customer = customers_service.get_customer_by_id(customers[0].customer_id)
    assert retrieved_customer is not None
    assert isinstance(retrieved_customer, Customer)
    assert retrieved_customer.name == customers[0].name
    assert retrieved_customer.email == customers[0].email
    assert retrieved_customer.phone_number == customers[0].phone_number


def test_get_customer_by_id_not_found(customers_service: CustomerService, customers: list[Customer]) -> None:
    with pytest.raises(CustomerNotFoundException):
        customers_service.get_customer_by_id(uuid.uuid4())


def test_create_customer(customers_service: CustomerService, create_customer_request: CustomerCreate) -> None:
    created_customer = customers_service.create_customer(customer=create_customer_request)
    assert created_customer is not None
    assert created_customer.name == create_customer_request.name
    assert created_customer.email == create_customer_request.email


def test_update_customer(customers_service: CustomerService, customers: list[Customer]) -> None:
    updated_customer = customers_service.update_customer(
        customer_id=customers[0].customer_id,
        customer=CustomerUpdate(email="updated_email@mail.com"),
    )
    assert updated_customer.email == "updated_email@mail.com"


def test_delete_customer(customers_service: CustomerService, customer_without_orders: Customer) -> None:
    customers_service.delete_customer(customer_id=customer_without_orders.customer_id)
    with pytest.raises(CustomerNotFoundException):
        customers_service.get_customer_by_id(customer_without_orders.customer_id)


def test_customer_check(customers_service: CustomerService, customer: Customer) -> None:
    customers_service.customer_check(customer.customer_id, 3)


def test_customer_check_is_ower(customers_service: CustomerService, customer_is_ower: Customer) -> None:
    with pytest.raises(CustomerIsOwerException):
        customers_service.customer_check(customer_is_ower.customer_id, 3)


def test_customer_check_reached_limit(customers_service: CustomerService, customer: Customer) -> None:
    with pytest.raises(CustomerReachedOrderLimitException):
        customers_service.customer_check(customer.customer_id, 5)
