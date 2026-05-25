"""
Seed script.
Insert sample data in database for user app exploration or testing.
"""
from datetime import date

from sqlmodel import Session

from database.database import engine
from database.models import Category, Transaction, Budget


def seed_data():

    with Session(engine) as session:

    # Insert transactions
        transactions = [

            # ---------- OCTOBER 2025 ----------
            Transaction(
                description="Apartment rent",
                amount=920,
                date=date(2025, 10, 3),
                category_id=1
            ),
            Transaction(
                description="Groceries Lidl",
                amount=64,
                date=date(2025, 10, 5),
                category_id=2
            ),
            Transaction(
                description="Dog food",
                amount=38,
                date=date(2025, 10, 7),
                category_id=7
            ),
            Transaction(
                description="Tennis club membership",
                amount=55,
                date=date(2025, 10, 10),
                category_id=8
            ),
            Transaction(
                description="Electricity bill",
                amount=82,
                date=date(2025, 10, 12),
                category_id=4
            ),
            Transaction(
                description="Cinema",
                amount=18,
                date=date(2025, 10, 18),
                category_id=6
            ),

            # ---------- NOVEMBER 2025 ----------
            Transaction(
                description="Apartment rent",
                amount=920,
                date=date(2025, 11, 3),
                category_id=1
            ),
            Transaction(
                description="Groceries Aldi",
                amount=71,
                date=date(2025, 11, 6),
                category_id=2
            ),
            Transaction(
                description="Dog vet visit",
                amount=94,
                date=date(2025, 11, 8),
                category_id=7
            ),
            Transaction(
                description="Train ticket",
                amount=46,
                date=date(2025, 11, 14),
                category_id=3
            ),
            Transaction(
                description="Internet bill",
                amount=39,
                date=date(2025, 11, 15),
                category_id=4
            ),
            Transaction(
                description="Restaurant",
                amount=42,
                date=date(2025, 11, 22),
                category_id=6
            ),

            # ---------- DECEMBER 2025 ----------
            Transaction(
                description="Apartment rent",
                amount=920,
                date=date(2025, 12, 3),
                category_id=1
            ),
            Transaction(
                description="Christmas gifts",
                amount=210,
                date=date(2025, 12, 18),
                category_id=6
            ),
            Transaction(
                description="Dog toys",
                amount=29,
                date=date(2025, 12, 20),
                category_id=7
            ),

            # ---------- JANUARY 2026 ----------
            Transaction(
                description="Apartment rent",
                amount=930,
                date=date(2026, 1, 3),
                category_id=1
            ),
            Transaction(
                description="Groceries Rewe",
                amount=68,
                date=date(2026, 1, 5),
                category_id=2
            ),
            Transaction(
                description="Tennis equipment",
                amount=89,
                date=date(2026, 1, 12),
                category_id=8
            ),
            Transaction(
                description="ETF",
                amount=1000,
                date=date(2026, 1, 12),
                category_id=10
            ),

            # ---------- FEBRUARY 2026 ----------
            Transaction(
                description="Apartment rent",
                amount=930,
                date=date(2026, 2, 3),
                category_id=1
            ),
            Transaction(
                description="Car Accident Repair",
                amount=300,
                date=date(2026, 2, 3),
                category_id=9
            ),
            Transaction(
                description="Dog insurance",
                amount=24,
                date=date(2026, 2, 10),
                category_id=5
            ),
            Transaction(
                description="Groceries",
                amount=73,
                date=date(2026, 2, 14),
                category_id=2
            ),

            # ---------- MARCH 2026 ----------
            Transaction(
                description="Apartment rent",
                amount=930,
                date=date(2026, 3, 3),
                category_id=1
            ),
            Transaction(
                description="Weekend trip",
                amount=145,
                date=date(2026, 3, 15),
                category_id=6
            )

        ]

        # Insert budgets
        budgets = [

            # ---------- OCTOBER 2025 ----------
            Budget(category_id=1, amount=950, date=date(2025, 10, 1)),
            Budget(category_id=2, amount=320, date=date(2025, 10, 1)),
            Budget(category_id=3, amount=120, date=date(2025, 10, 1)),
            Budget(category_id=4, amount=180, date=date(2025, 10, 1)),
            Budget(category_id=5, amount=90, date=date(2025, 10, 1)),
            Budget(category_id=6, amount=220, date=date(2025, 10, 1)),
            Budget(category_id=7, amount=90, date=date(2025, 10, 1)),
            Budget(category_id=8, amount=80, date=date(2025, 10, 1)),
            Budget(category_id=9, amount=50, date=date(2025, 10, 1)),

            # ---------- NOVEMBER 2025 ----------
            Budget(category_id=1, amount=950, date=date(2025, 11, 1)),
            Budget(category_id=2, amount=320, date=date(2025, 11, 1)),
            Budget(category_id=3, amount=120, date=date(2025, 11, 1)),
            Budget(category_id=4, amount=180, date=date(2025, 11, 1)),
            Budget(category_id=5, amount=90, date=date(2025, 11, 1)),
            Budget(category_id=6, amount=220, date=date(2025, 11, 1)),
            Budget(category_id=7, amount=90, date=date(2025, 11, 1)),
            Budget(category_id=8, amount=80, date=date(2025, 11, 1)),
            Budget(category_id=9, amount=50, date=date(2025, 11, 1)),

            # ---------- DECEMBER 2025 ----------
            Budget(category_id=1, amount=950, date=date(2025, 12, 1)),
            Budget(category_id=2, amount=340, date=date(2025, 12, 1)),
            Budget(category_id=3, amount=120, date=date(2025, 12, 1)),
            Budget(category_id=4, amount=190, date=date(2025, 12, 1)),
            Budget(category_id=5, amount=90, date=date(2025, 12, 1)),
            Budget(category_id=6, amount=350, date=date(2025, 12, 1)),
            Budget(category_id=7, amount=100, date=date(2025, 12, 1)),
            Budget(category_id=8, amount=80, date=date(2025, 12, 1)),
            Budget(category_id=9, amount=50, date=date(2025, 12, 1)),

            # ---------- JANUARY 2026 ----------
            Budget(category_id=1, amount=960, date=date(2026, 1, 1)),
            Budget(category_id=2, amount=320, date=date(2026, 1, 1)),
            Budget(category_id=3, amount=120, date=date(2026, 1, 1)),
            Budget(category_id=4, amount=200, date=date(2026, 1, 1)),
            Budget(category_id=5, amount=90, date=date(2026, 1, 1)),
            Budget(category_id=6, amount=200, date=date(2026, 1, 1)),
            Budget(category_id=7, amount=90, date=date(2026, 1, 1)),
            Budget(category_id=8, amount=80, date=date(2026, 1, 1)),
            Budget(category_id=9, amount=50, date=date(2026, 1, 1)),

            # ---------- FEBRUARY 2026 ----------
            Budget(category_id=1, amount=960, date=date(2026, 2, 1)),
            Budget(category_id=2, amount=310, date=date(2026, 2, 1)),
            Budget(category_id=3, amount=120, date=date(2026, 2, 1)),
            Budget(category_id=4, amount=210, date=date(2026, 2, 1)),
            Budget(category_id=5, amount=90, date=date(2026, 2, 1)),
            Budget(category_id=6, amount=200, date=date(2026, 2, 1)),
            Budget(category_id=7, amount=90, date=date(2026, 2, 1)),
            Budget(category_id=8, amount=80, date=date(2026, 2, 1)),
            Budget(category_id=9, amount=50, date=date(2026, 2, 1)),

            # ---------- MARCH 2026 ----------
            Budget(category_id=1, amount=960, date=date(2026, 3, 1)),
            Budget(category_id=2, amount=320, date=date(2026, 3, 1)),
            Budget(category_id=3, amount=120, date=date(2026, 3, 1)),
            Budget(category_id=4, amount=190, date=date(2026, 3, 1)),
            Budget(category_id=5, amount=90, date=date(2026, 3, 1)),
            Budget(category_id=6, amount=240, date=date(2026, 3, 1)),
            Budget(category_id=7, amount=90, date=date(2026, 3, 1)),
            Budget(category_id=8, amount=80, date=date(2026, 3, 1)),
            Budget(category_id=9, amount=50, date=date(2026, 3, 1)),

        ]

        session.add_all(transactions)
        session.add_all(budgets)

        session.commit()

        print("Database seeded successfully")


if __name__ == "__main__":
    seed_data()