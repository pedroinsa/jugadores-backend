from sqlalchemy.orm import Session
from models import  User
#returns all users
def get_all_users(db: Session, skip: int = 0, limit: int = 20):
    return db.query(User).offset(skip).limit(limit).all()
#returns all users actives
def get_all_users_actives(db: Session, skip: int = 0, limit : int = 20):
     return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
#returns all users that match the username or a fragment of the username
def get_users_by_username (db: Session, username: str, skip: int = 0, limit : int = 20):
     return db.query(User).filter(User.username.ilike(f"%{username}%") ).offset(skip).limit(limit).all()
#returns all users that match the email or a fragment of the email
def get_users_by_email (db: Session, email: str, skip: int = 0, limit : int = 20):
     return db.query(User).filter(User.email.ilike(f"%{email}%") ).offset(skip).limit(limit).all()
# returns a user by username
def get_user_by_username (db: Session, username: str):
     return db.query(User).filter(User.username == username).first()
#returns a user by id
def get_user_by_id (db: Session, id: int):
    return db.query(User).filter(User.id == id).first()
#returns a user by email
def get_user_by_email (db: Session, email: str):
     return db.query(User).filter(User.email== email).first()


