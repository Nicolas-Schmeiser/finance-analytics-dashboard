"""
Response schemas for API endpoints.

These models define the structure of data returned by the API.
They are not database tables.
"""

from datetime import date
from decimal import Decimal
from sqlmodel import SQLModel


class TransactionWithCategory(SQLModel):
    """
    API response model.

    Represents a transaction including the category name.
    """

    id: int
    description: str
    amount: Decimal
    date: date
    category: str


class CategorySummary(SQLModel):

    year_month: str
    category: str
    spent: Decimal
    budget: Decimal
