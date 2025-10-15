# Import the create_engine function from SQLAlchemy.
# This is used to create the connection to the database.
from sqlalchemy import create_engine

# Import sessionmaker and declarative_base from SQLAlchemy.
# sessionmaker → used to create sessions to interact with the database.
# declarative_base → base class used to create models (tables).
from sqlalchemy.orm import sessionmaker, declarative_base


# Define the database URL
# sqlite:///./obras.db → SQLite database named obras.db in the same project folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./obras.db"

# Create the database connection engine
# connect_args={"check_same_thread": False} is required only when using SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a "session factory"
# Every time we want to interact with the database, we use SessionLocal()
SessionLocal = sessionmaker(
    autocommit=False,   # ensures changes only happen after commit()
    autoflush=False,    # prevents automatic saving (gives more manual control)
    bind=engine         # connects to the engine created above
)


# Create the base class for the models (tables)
# All models in the project will inherit from this Base
Base = declarative_base()


'''

create_engine → connects Python to the database.

sessionmaker → creates sessions that we use to read/write data.

declarative_base → allows us to create classes that will become database tables.

SQLALCHEMY_DATABASE_URL → tells SQLAlchemy where the database is stored.

SessionLocal → we use it to get a session whenever we need the database.

--- Without flush, you'll only see the ID after the commit.

With flush, SQLAlchemy already sends the data to the database 
and generates the ID, but it's still possible to roll back before committing.
'''
