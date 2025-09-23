from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from sqlalchemy.pool import StaticPool
from env import DATABASE_URL



engine  = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

SessionConnect = sessionmaker(autoflush=False, bind=engine)

    
def get_test_db():
    db = SessionConnect()
    try:
        yield db
    finally:
        db.close()




