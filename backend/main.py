from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

from sqlmodel import Session, select
from database.database import engine
from database.models import Transaction, Category
from database.schemas import TransactionWithCategory

from datetime import date
    
app = FastAPI()

# Add CORS middleware otherwise the frontend won't be able to access the API response due to CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root route to confirm API is running when starting the server
@app.get("/") 
def root():
    return {"message": "API is running"}


# Dynamic load of existing categories in filter
@app.get("/categories", response_model=list[Category]) 
def get_categories():

    with Session(engine) as session:

        statement = (select(Category))
        results = session.exec(statement).all()

        return results


# Main endpoint to get filtered transaction data
# response model defines the structure of the API response, included in docs
@app.get("/transactions", response_model=list[TransactionWithCategory]) 
def get_transactions(
    # Filters
    category: str | None = Query(default=None),
    min_amount: float | None = Query(default=None),
    max_amount: float | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
):

    with Session(engine) as session:

        # Get all transactions
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

        if max_amount is not None:
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

        # Return transactions using reponse model
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
    

# Edit category from an existing transaction
@app.put("/transactions/{transaction_id}/category")
def update_transaction_category(
    transaction_id: int,
    category_id: int
):
    with Session(engine) as session:

        # Select relevant transaction record
        transaction = session.get(Transaction, transaction_id)

        if not transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        # Change category to new value
        transaction.category_id = category_id

        # Update database
        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        return transaction