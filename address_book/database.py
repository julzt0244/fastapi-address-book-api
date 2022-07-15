from enum import Enum, auto

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DatabaseEnv(Enum):
    Prod = auto()
    Test = auto()


def create_db_engine_and_session(database_mode: DatabaseEnv = DatabaseEnv.Prod):
    if database_mode is DatabaseEnv.Prod:
        db_name = "AddressBookDB"
    else:
        db_name = "TestDB"

    SQLALCHEMY_DATABASE_URL = f"sqlite:///./{db_name}.db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return engine, SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


engine, SessionLocal = create_db_engine_and_session()

Base = declarative_base()
