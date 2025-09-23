from sqlalchemy.orm import Session
from models import Comment
import schemas


#create comment

def create_comment(db:Session, comment: schemas.CommentCreate, post_id: int, user_id: int):
    new_comment = Comment(content = comment.content, post_id = post_id, user_id = user_id )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment