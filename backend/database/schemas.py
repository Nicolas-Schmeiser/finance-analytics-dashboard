"""
Response schemas for API endpoints.

These models define the structure of data returned by the API.
They are not database tables.
"""

from datetime import date
from sqlmodel import SQLModel


class TransactionWithCategory(SQLModel):
    """
    API response model.

    Represents a transaction including the category name.
    """

    id: int
    description: str
    amount: int
    date: date
    category_id: int
    category_name: str


class CategorySpendWithBudget(SQLModel):

    category: str
    spent: int
    budget: int

class MonthlyTotalSpend(SQLModel):

    year_month: str
    spent: int