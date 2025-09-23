from sqlalchemy.orm import Session
from models import Comment
import schemas


#modify comment

def modify_comment(db: Session, comment: Comment, update_comment: schemas.CommentModify):
          
    updating_comment =  update_comment.model_dump(exclude_unset=True)
    for key, value in updating_comment.items():
        setattr(comment,key, value)
    db.commit()
    db.refresh(comment)
    return comment
    
