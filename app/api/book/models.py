import uuid

from sqlmodel import Field, SQLModel


class BookCreateUpdate(SQLModel):
    title: str = Field()
    author: str = Field()
    genre: str = Field()
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)


class Book(BookCreateUpdate, table=True):
    __tablename__ = "books"

    book_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
