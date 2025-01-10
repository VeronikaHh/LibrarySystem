import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status

from .models import Order, OrderUpdate, OrderCreate
from .service import OrderService

router = APIRouter(prefix="/orders", tags=["Order"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_orders(order_service: Annotated[OrderService, Depends()]) -> list[Order]:
    return order_service.get_all_orders()


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order_by_id(
        order_id: uuid.UUID,
        order_service: Annotated[OrderService, Depends()],
) -> Order:
    return order_service.get_order_by_id(order_id=order_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_order(
        order: OrderCreate,
        order_service: Annotated[OrderService, Depends()],
) -> Order:
    return order_service.create_order(order=order)


@router.put("/{order_id}", status_code=status.HTTP_200_OK)
async def update_order(
        order_id: uuid.UUID,
        order: OrderUpdate,
        order_service: Annotated[OrderService, Depends()],
) -> Order:
    return order_service.update_order(order_id=order_id, order=order)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
        order_id: uuid.UUID,
        order_service: Annotated[OrderService, Depends()],
) -> None:
    return order_service.delete_order(order_id=order_id)


@router.patch("/{order_id}/close", status_code=status.HTTP_200_OK)
async def close_order(
        order_id: uuid.UUID,
        order_service: Annotated[OrderService, Depends()],
) -> Order:
    return order_service.close_order(order_id=order_id)
