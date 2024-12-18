import uuid

from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    __tablename__ = "books"

    book_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field()
    author: str = Field()
    genre: str = Field()
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)