from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from typing import List
from utils.utils import get_current_user
from crud.comments.crud_get import get_all_comments_from_post
from crud.posts.crud_get import get_post_by_post_id


router = APIRouter()

@router.get("/allcomments/{post_id}/values", response_model= List[schemas.CommentResponse])
def get_all_commments_function(post_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db), 
                               current_user: models.User = Depends(get_current_user)):
        post = get_post_by_post_id(db, post_id)
        if not post:
                raise HTTPException(status_code=404, detail="No existe este post en la base de datos")
        comments = get_all_comments_from_post(db, post_id, skip, limit)

        return comments
        


   