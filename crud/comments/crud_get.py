from sqlalchemy.orm import Session, joinedload
from models import Comment
import schemas

#returns all comments from post

def get_all_comments_from_post(db: Session, post_id: int, skip: int = 0, limit: int = 20):
   return db.query(Comment).options(joinedload(Comment.user)).filter(Comment.post_id == post_id).order_by(Comment.id.desc()).offset(skip).limit(limit).all()


#returns all comnents by content
def get_comments_by_content(db: Session, content: str, skip: int = 0, limit: int = 20):

    return db.query(Comment).options(joinedload(Comment.user)).filter(Comment.content.ilike(f"%{content}%")).order_by(Comment.id.desc()).offset(skip).limit(limit).all()

#return comment by comment_id
def get_comment_by_comment_id(db: Session, comment_id: int):
    return db.query(Comment).options(joinedload(Comment.user)).filter(Comment.id == comment_id).first()