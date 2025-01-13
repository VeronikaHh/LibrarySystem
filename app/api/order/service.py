import uuid
from typing import Annotated

from fastapi import Depends

from app.api.book import BookDataAccessLayer
from app.api.customer import CustomerService
from .dal import OrderDataAccessLayer
from .models import Order, OrderUpdate, OrderCreate


class OrderService:
    def __init__(
            self,
            order_dal: Annotated[OrderDataAccessLayer, Depends()],
            book_dal: Annotated[BookDataAccessLayer, Depends()],
            customer_service: Annotated[CustomerService, Depends()],
    ) -> None:
        self.order_dal = order_dal
        self.book_dal = book_dal
        self.customer_service = customer_service

    def get_all_orders(self) -> list[Order]:
        return list(self.order_dal.get_all_orders())

    def get_order_by_id(self, order_id: uuid.UUID) -> Order:
        return self.order_dal.get_order_by_id(order_id)

    def create_order(self, order: OrderCreate) -> Order:
        customer_orders = self.order_dal.get_orders_for_customer(customer_id=order.customer_id, returned=False)
        self.customer_service.customer_check(customer_id=order.customer_id, orders_quantity=len(customer_orders))
        self.book_dal.check_available(book_id=order.book_id)
        created_order = self.order_dal.create_order(order)
        self.book_dal.decrement_book_quantity(book_id=order.book_id)
        return created_order

    def update_order(self, order_id: uuid.UUID, order: OrderUpdate) -> Order:
        return self.order_dal.update_order(order_id, order)

    def delete_order(self, order_id: uuid.UUID) -> None:
        return self.order_dal.delete_order(order_id)

    def close_order(self, order_id: uuid.UUID) -> Order:
        order = self.order_dal.close_order(order_id)
        self.book_dal.increment_book_quantity(book_id=order.book_id)
        return order
