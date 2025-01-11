import pytest
from sqlmodel import Session

from app.api.book import Book, BookDataAccessLayer
from app.api.customer import Customer, CustomerService
from app.api.employee import Employee
from app.api.order import Order, OrderCreate, OrderDataAccessLayer, OrderService


@pytest.fixture(scope="session")
def orders_dal(
        test_database_session: Session,
) -> OrderDataAccessLayer:
    return OrderDataAccessLayer(
        session=test_database_session,
    )


@pytest.fixture(scope="session")
def orders_service(
        orders_dal: OrderDataAccessLayer,
        books_dal: BookDataAccessLayer,
        customers_service: CustomerService,
) -> OrderService:
    return OrderService(
        order_dal=orders_dal,
        book_dal=books_dal,
        customer_service=customers_service,
    )


@pytest.fixture(scope="module")
def orders(
        orders_dal: OrderDataAccessLayer,
        books: list[Book],
        customers_with_orders: list[Customer],
        employee_with_orders: Employee,
) -> list[Order]:
    old_orders = orders_dal.get_all_orders()
    for order in old_orders:
        orders_dal.delete_order(order.order_id)

    # ------alternative way------
    # statement = delete(Order)
    # test_database_session.exec(statement)
    # test_database_session.commit()

    sample_orders = [
        Order(
            customer_id=customers_with_orders[i].customer_id,
            book_id=books[i].book_id,
            employee_id=employee_with_orders.employee_id,
        ) for i in range(2)
    ]
    for order in sample_orders:
        orders_dal.create_order(order)
    return sample_orders


@pytest.fixture(scope="function")
def order(
        orders_dal: OrderDataAccessLayer,
        books: list[Book],
        customers_with_orders: list[Customer],
        employee_with_orders: Employee,
) -> Order:
    order = Order(
        customer_id=customers_with_orders[0].customer_id,
        book_id=books[0].book_id,
        employee_id=employee_with_orders.employee_id,
    )
    orders_dal.create_order(order)
    return order


@pytest.fixture(scope="module")
def create_order_request(
        books: list[Book],
        customers_with_orders: list[Customer],
        employee_with_orders: Employee,
) -> OrderCreate:
    return OrderCreate(
        customer_id=customers_with_orders[0].customer_id,
        book_id=books[1].book_id,
        employee_id=employee_with_orders.employee_id,
    )
