import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from db_config import get_database_session
from .exceptions import OrderNotFoundError, InvalidOrderDataError
from .models import Order, OrderUpdate, OrderCreate

router = APIRouter(prefix="/orders", tags=["Order"])


@router.get("", status_code=200)
async def get_orders(session: Annotated[Session, Depends(get_database_session)]):
    db_orders = session.exec(select(Order)).all()
    return db_orders


@router.get("/{order_id}", status_code=200)
async def get_order_by_id(order_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    db_order = session.get(Order, order_id)
    if db_order is None:
        raise OrderNotFoundError(order_id=order_id)
    return db_order


@router.post("", status_code=201)
async def create_order(order: OrderCreate, session: Annotated[Session, Depends(get_database_session)]):
    db_order = Order(**order.model_dump())
    try:
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
    except IntegrityError as err:
        raise InvalidOrderDataError(order_id=order.order_id, error=str(err))
    return db_order


@router.put("/{order_id}", status_code=201)
async def update_order(order_id: uuid.UUID, order: OrderUpdate,
                       session: Annotated[Session, Depends(get_database_session)]):
    db_order = session.get(Order, order_id)
    if db_order is None:
        raise OrderNotFoundError(order_id=order_id)
    try:
        db_order.sqlmodel_update(order.model_dump())
        session.commit()
        session.refresh(db_order)
    except IntegrityError as err:
        raise InvalidOrderDataError(order_id=order.order_id, error=str(err))
    return db_order


@router.delete("/{order_id}", status_code=200)
async def delete_order(order_id: uuid.UUID, session: Annotated[Session, Depends(get_database_session)]):
    order = session.get(Order, order_id)
    if not order:
        raise OrderNotFoundError(order_id=order_id)
    session.delete(order)
    session.commit()
    return {"ok": True}
