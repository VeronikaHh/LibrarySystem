import uuid

from sqlalchemy import Column, VARCHAR
from sqlmodel import Field, SQLModel

from app.api.book.constants import Genres


class BookUpdate(SQLModel):
    title: str | None = None
    author: str | None = None
    genre: Genres | None = Field(sa_column=Column(VARCHAR, default=None))
    price: float | None = Field(default=None, ge=0)
    quantity: int | None = Field(default=None, ge=0)


class BookCreate(SQLModel):
    title: str = Field()
    author: str = Field()
    genre: Genres = Field(sa_column=Column(VARCHAR, nullable=False))
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)


class Book(BookCreate, table=True):
    __tablename__ = "books"

    book_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
