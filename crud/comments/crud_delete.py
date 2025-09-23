from sqlalchemy.orm import Session
from models import Comment
import schemas

#delete comment

def delete_comment(db: Session, comment: Comment):

    db.delete(comment)
    db.commit()

    return "El comentario fue eliminado"