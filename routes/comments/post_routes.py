from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from typing import List
from utils.utils import get_current_user
from crud.comments.crud_post import create_comment
from crud.posts.crud_get import get_post_by_post_id
from checkers.checker_comments import validate_content_comment


router = APIRouter()

@router.post("/createcomment/{post_id}")
def create_comment_function(post_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user) ):

    post: models.Post | None = get_post_by_post_id(db, post_id)
    if not post:
        raise HTTPException(status_code = 404, detail= "No existe el post solicitado")
    content_comment_validated = validate_content_comment(comment.content)
    schema_validated = schemas.CommentCreate(content = content_comment_validated)
    
    comment_created = create_comment(db,schema_validated,post_id, current_user.id)

    return comment_created

    


    
