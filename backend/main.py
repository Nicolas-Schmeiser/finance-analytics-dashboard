from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

from sqlmodel import Session, select
from database.database import engine
from database.models import Transaction, Category, Budget
from database.schemas import TransactionWithCategory, CategorySpendWithBudget, MonthlyTotalSpend
from sqlalchemy import func

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


# Filtered transaction data
@app.get("/transactions", response_model=list[TransactionWithCategory]) 
def get_transactions(
    # Filters
    category_id: int | None = Query(default=None),
    min_amount: int | None = Query(default=None),
    max_amount: int | None = Query(default=None),
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

        # Filters
        if category_id is not None:
            statement = statement.where(Category.id == category_id)

        if min_amount is not None:
            statement = statement.where(Transaction.amount >= min_amount)

        if max_amount is not None: 
            statement = statement.where(Transaction.amount <= max_amount)
            
        if start_date is not None:
            statement = statement.where(Transaction.date >= start_date)

        if end_date is not None:
            statement = statement.where(Transaction.date <= end_date)

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
                    category_id=transaction.category_id,
                    category_name=category_name
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
    

# Filtered aggregated monthly sum of transaction amount and budget per category
@app.get("/category_spend_with_budget", response_model=list[CategorySpendWithBudget]) 
def get_category_spend_with_budget(
    # Filters
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
):
    
    start_month = start_date.strftime("%Y-%m") if start_date else None
    end_month = end_date.strftime("%Y-%m") if end_date else None

    with Session(engine) as session:

        transaction_subq = (
            select(
                Category.id.label("category_id"), # type: ignore
                func.sum(Transaction.amount).label("spent")
            )
            .join(Category, Category.id == Transaction.category_id) # type: ignore
            .group_by(Category.id) # type: ignore
        )

        if start_date is not None:
            transaction_subq = transaction_subq.where(
                Transaction.date >= start_date
            )

        if end_date is not None:
            transaction_subq = transaction_subq.where(
                Transaction.date <= end_date
            )

        transaction_subq = transaction_subq.subquery()

        budget_subq = (
            select(
                Category.id.label("category_id"), # type: ignore
                func.sum(Budget.amount).label("budget")
            )
            .join(Category, Category.id == Budget.category_id) # type: ignore
            .group_by(Category.id) # type: ignore
        )

        if start_month is not None:
            budget_subq = budget_subq.where(
                func.strftime("%Y-%m", Budget.date) >= start_month
            )

        if end_month is not None:
            budget_subq = budget_subq.where(
                func.strftime("%Y-%m", Budget.date) <= end_month
            )

        budget_subq = budget_subq.subquery()

        statement = (
            select(
                Category.name,
                func.coalesce(transaction_subq.c.spent, 0),
                func.coalesce(budget_subq.c.budget, 0)
            )
            .select_from(Category)
            .outerjoin(transaction_subq, Category.id == transaction_subq.c.category_id) # type: ignore
            .outerjoin(budget_subq, Category.id == budget_subq.c.category_id) # type: ignore
            .order_by(Category.name)
        )

        results = session.exec(statement).all()

        output = []

        # Return transactions using reponse model
        for category, spent, budget in results:
            output.append(
                CategorySpendWithBudget(
                    category = category,
                    spent = spent,
                    budget = budget
                )
            )

        return output
    

    # Filtered aggregated monthly sum of transaction amount and budget per category
@app.get("/monthly_total_spend", response_model=list[MonthlyTotalSpend]) 
def get_monthly_total_spend(
    # Filters
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
):

    with Session(engine) as session:

        year_month = func.strftime(
            "%Y-%m",
            Transaction.date
        )

        statement = (
            select(
                year_month.label("year_month"),
                func.coalesce(func.sum(Transaction.amount),0).label("spent"),
            )
            .select_from(Transaction)
            .group_by(year_month)
            .order_by(year_month)
        )

        # Apply filter only if parameter is provided
        if start_date is not None:
            statement = statement.where(
                Transaction.date >= start_date
            )

        if end_date is not None:
            statement = statement.where(
                Transaction.date <= end_date
            )

        results = session.exec(statement).all()

        output = []

        # Return transactions using reponse model
        for year_month, spent in results:
            output.append(
                MonthlyTotalSpend(
                    year_month = year_month,
                    spent = spent
                )
            )

        return output