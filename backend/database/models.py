"""
Database models (tables). Equivalent to SQL scehema definitions.

Each class represents one table in the database.
"""

from datetime import date # required for date fields
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey, Numeric

class Category(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True) # 'None' required for autoincrementing primary keys
    name: str = Field(max_length=50)


class Transaction(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)
    description: str
    amount: float = Field(sa_column=Column(Numeric(12, 2), nullable=False))
    date: date

    category_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "category.id",
                ondelete="RESTRICT",
                onupdate="CASCADE"
            ),
            nullable=False
        )
    )


class Budget(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)
    amount: int
    date: date

    category_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "category.id",
                ondelete="CASCADE",
                onupdate="CASCADE"
            ),
            nullable=False
        )
    )