import uuid
from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.db_config import get_database_session
from .exceptions import OrderNotFoundException, InvalidOrderDataException
from .models import Order, OrderCreate, OrderUpdate


class OrderDataAccessLayer:
    def __init__(self, session: Annotated[Session, Depends(get_database_session)]) -> None:
        self.__session = session

    def get_all_orders(self) -> Sequence[Order]:
        return self.__session.exec(select(Order)).all()

    def get_order_by_id(self, order_id: uuid.UUID) -> Order:
        statement = select(Order).where(Order.order_id == order_id)
        db_order = self.__session.exec(statement).one_or_none()
        if db_order is None:
            raise OrderNotFoundException(order_id=order_id)
        return db_order

    def create_order(self, order: OrderCreate) -> Order:
        db_order = Order(**order.model_dump())
        try:
            self.__session.add(db_order)
            self.__session.commit()
            self.__session.refresh(db_order)
        except IntegrityError as err:
            raise InvalidOrderDataException(order_id=db_order.order_id, error=str(err))
        return db_order

    def update_order(self, order_id: uuid.UUID, order: OrderUpdate) -> Order:
        db_order = self.get_order_by_id(order_id)
        try:
            db_order.sqlmodel_update(order.model_dump(exclude_none=True))
            self.__session.commit()
            self.__session.refresh(db_order)
        except IntegrityError as err:
            raise InvalidOrderDataException(order_id=order_id, error=str(err))
        return db_order

    def delete_order(self, order_id: uuid.UUID) -> None:
        db_order = self.get_order_by_id(order_id)
        try:
            self.__session.delete(db_order)
            self.__session.commit()
        except IntegrityError as err:
            raise InvalidOrderDataException(order_id=order_id, error=str(err))

    def close_order(self, order_id: uuid.UUID) -> Order:
        db_order = self.get_order_by_id(order_id)
        db_order.is_returned = True
        self.__session.commit()
        self.__session.refresh(db_order)
        return db_order
