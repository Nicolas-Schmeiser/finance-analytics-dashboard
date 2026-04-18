from fastapi import FastAPI

from sqlmodel import Session, select
from database.database import engine
from database.models import Transaction, Category
from database.schemas import TransactionWithCategory

app = FastAPI()

@app.get("/transactions", response_model=list[TransactionWithCategory]) # response model defines the structure of the API response, included in docs
def get_transactions():

    with Session(engine) as session:

        statement = (
            select(
                Transaction,
                Category.name
            )
            .select_from(Transaction)
            .join(
                Category,
                Transaction.category_id == Category.id  # type: ignore (ignore type error from SQLModel's join syntax)
            )
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