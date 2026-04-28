from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import Session, select
from database.database import engine
from database.models import Transaction, Category
from database.schemas import TransactionWithCategory

from datetime import date
    
app = FastAPI()

# Add CORS middleware otherwise the frontend won't be able to access the API response due to CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow project defined frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/") # Root route to confirm API is running when starting the server
def root():
    return {"message": "API is running"}


@app.get("/categories", response_model=list[str]) # Dynamic load of existing categories in filter
def get_categories():

    with Session(engine) as session:

        statement = (select(Category.name))
        results = session.exec(statement).all()

        return results


@app.get("/transactions", response_model=list[TransactionWithCategory]) # response model defines the structure of the API response, included in docs
def get_transactions(
    category: str | None = Query(default=None),
    min_amount: float | None = Query(default=None),
    max_amount: float | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    ):

    with Session(engine) as session:

        statement = (
            select(
                Transaction,
                Category.name
            )
            .select_from(Transaction)
            .join(
                Category,
                Transaction.category_id == Category.id # type: ignore
            )
        )

        # Apply filter only if parameter is provided
        if category:
            statement = statement.where(
                Category.name == category
            )

        if min_amount is not None: # To ensure 0 would not be considered as FALSE
            statement = statement.where(
                Transaction.amount >= min_amount
            )

        if max_amount is not None: # To ensure 0 would not be considered as FALSE
            statement = statement.where(
                Transaction.amount <= max_amount
        )
            
        if start_date is not None:
            statement = statement.where(
                Transaction.date >= start_date
            )

        if end_date is not None:
            statement = statement.where(
                Transaction.date <= end_date
            )

        results = session.exec(statement).all()

        transactions = []

        for transaction, category_name in results:

            transactions.append(
                TransactionWithCategory(
                    id=transaction.id, # type: ignore
                    description=transaction.description,
                    amount=transaction.amount,
                    date=transaction.date,
                    category=category_name
                )
            )

        return transactions