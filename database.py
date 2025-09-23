from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from contextlib import contextmanager
from env import URL_CONNECTION


engine  = create_engine(URL_CONNECTION)


SessionConnect = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionConnect()
    try:
        yield db
    finally:
        db.close()
