import uuid

import pytest

from app.api.customer import Customer, CustomerUpdate, CustomerDataAccessLayer, CustomerNotFoundException, \
    CustomerCreate


def test_get_all_customers(customers_dal: CustomerDataAccessLayer, customers: list[Customer]) -> None:
    result = customers_dal.get_all_customers()
    assert len(result) == 2
    for item in result:
        assert isinstance(item, Customer)


def test_get_customer_by_id(customers_dal: CustomerDataAccessLayer, customers: list[Customer]) -> None:
    retrieved_customer = customers_dal.get_customer_by_id(customers[0].customer_id)
    assert retrieved_customer is not None
    assert isinstance(retrieved_customer, Customer)
    assert retrieved_customer.name == customers[0].name
    assert retrieved_customer.email == customers[0].email
    assert retrieved_customer.phone_number == customers[0].phone_number
    assert retrieved_customer.is_ower == customers[0].is_ower


def test_get_customer_by_id_not_found(customers_dal: CustomerDataAccessLayer, customers: list[Customer]) -> None:
    with pytest.raises(CustomerNotFoundException):
        customers_dal.get_customer_by_id(uuid.uuid4())


def test_create_customer(customers_dal: CustomerDataAccessLayer, create_customer_request: CustomerCreate) -> None:
    created_customer = customers_dal.create_customer(customer=create_customer_request)
    assert created_customer is not None
    assert created_customer.name == create_customer_request.name
    assert created_customer.email == create_customer_request.email


def test_update_customer(customers_dal: CustomerDataAccessLayer, customers: list[Customer]) -> None:
    updated_customer = customers_dal.update_customer(
        customer_id=customers[0].customer_id,
        customer=CustomerUpdate(email="updated_email@mail.com"),
    )
    assert updated_customer.email == "updated_email@mail.com"


def test_delete_customer(customers_dal: CustomerDataAccessLayer, customers: list[Customer]) -> None:
    customers_dal.delete_customer(customer_id=customers[0].customer_id)
    with pytest.raises(CustomerNotFoundException):
        customers_dal.get_customer_by_id(customers[0].customer_id)
