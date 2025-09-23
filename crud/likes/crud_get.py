from sqlalchemy.orm import Session
from models import Like


#returns all likes from user

def get_all_likes_from_user(db: Session, user_id: int):
    return db.query(Like).filter(Like.user_id  == user_id).all()

#returns all likes from post

def get_all_likes_from_post(db: Session, post_id : int):
    return db.query(Like).filter(Like.post_id == post_id).order_by(Like.created_at.desc()).all()


#returns like by like_id

def get_like_by_like_id(db: Session, like_id: int):
    return db.query(Like).filter(Like.id == like_id).first()
    