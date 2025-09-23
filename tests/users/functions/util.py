from models import User
from sqlalchemy.orm import Session
from fastapi import Depends
from tests.db_test import get_test_db

def make_override_get_current_user(username: str, db: Session):
     def _overrides():
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise Exception(f"User {username} no existe en la base de datos de testing")
        
        user = db.merge(user)
        return user
     return _overrides