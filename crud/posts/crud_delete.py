from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Post


#delete post

def delete_post (db: Session, post: Post, post_id: int):
     
     db.delete(post)
     db.commit()
     return "El post fue eliminado"