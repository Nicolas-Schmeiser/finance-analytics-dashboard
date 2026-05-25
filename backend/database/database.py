"""
Database configuration.

Creates the SQLite database connection and
provides a function to initialize tables.
"""

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Session, create_engine, select

from database.models import Category

# SQLite database file location
DATABASE_URL = "sqlite:///database/finance.db"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Enable SQLite foreign key constraints
@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def create_default_categories():
    """
    Insert default categories only if none exist.
    """

    with Session(engine) as session:

        existing_category = session.exec(
            select(Category)
        ).first()

        if not existing_category:

            categories = [
                Category(name="Rent"),
                Category(name="Groceries"),
                Category(name="Transport"),
                Category(name="Utilities"),
                Category(name="Insurance"),
                Category(name="Leisure"),
                Category(name="Dog"),
                Category(name="Tennis"),
                Category(name="Misc"),
                Category(name="Investment")
            ]

            session.add_all(categories)
            session.commit()

def create_db_and_tables():
    """
    Create all tables defined in models.
    """

    SQLModel.metadata.create_all(engine)
    create_default_categories()