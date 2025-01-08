import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status

from app.api.book import BookDataAccessLayer
from .dal import OrderDataAccessLayer
from .models import Order, OrderUpdate, OrderCreate

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
) -> Order:
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
