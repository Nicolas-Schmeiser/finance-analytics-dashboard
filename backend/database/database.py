"""
Database configuration.

Creates the SQLite database connection and
provides a function to initialize tables.
"""

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, create_engine

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


def create_db_and_tables():
    """
    Create all tables defined in models.
    This runs once when initializing the database.
    """
    SQLModel.metadata.create_all(engine)