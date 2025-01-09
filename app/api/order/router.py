import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status

from app.api.book import BookDataAccessLayer
from .dal import OrderDataAccessLayer
from .models import Order, OrderUpdate, OrderCreate
from app.api.customer import CustomerDataAccessLayer

router = APIRouter(prefix="/orders", tags=["Order"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_orders(order_dal: Annotated[OrderDataAccessLayer, Depends()]) -> list[Order]:
    return list(order_dal.get_all_orders())


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order_by_id(order_id: uuid.UUID, order_dal: Annotated[OrderDataAccessLayer, Depends()]) -> Order:
    return order_dal.get_order_by_id(order_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_order(
        order: OrderCreate,
        order_dal: Annotated[OrderDataAccessLayer, Depends()],
        book_dal: Annotated[BookDataAccessLayer, Depends()],
        customer_dal: Annotated[CustomerDataAccessLayer, Depends()],
) -> Order:
    customer_orders = order_dal.get_orders_for_customer(customer_id=order.customer_id, returned=False)
    customer_dal.customer_check(customer_id=order.customer_id, orders_quantity=len(customer_orders))
    book_dal.check_available(book_id=order.book_id)
    created_order = order_dal.create_order(order)
    book_dal.decrement_book_quantity(book_id=order.book_id)
    return created_order


@router.put("/{order_id}", status_code=status.HTTP_200_OK)
async def update_order(
        order_id: uuid.UUID,
        order: OrderUpdate,
        order_dal: Annotated[OrderDataAccessLayer, Depends()],
) -> Order:
    return order_dal.update_order(order_id, order)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: uuid.UUID, order_dal: Annotated[OrderDataAccessLayer, Depends()]) -> None:
    return order_dal.delete_order(order_id)

@router.patch("/{order_id}/close", status_code=status.HTTP_200_OK)
async def close_order(
        order_id: uuid.UUID,
        order_dal: Annotated[OrderDataAccessLayer, Depends()],
        book_dal: Annotated[BookDataAccessLayer, Depends()],
) -> Order:
    order = order_dal.close_order(order_id)
    book_dal.increment_book_quantity(book_id=order.book_id)
    return order
