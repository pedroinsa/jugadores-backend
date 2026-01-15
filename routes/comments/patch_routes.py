from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from typing import List
from utils.utils import get_current_user
from crud.comments.crud_get import get_comment_by_comment_id
from checkers.checker_comments import validate_content_comment
from crud.comments.crud_patch import modify_comment


router = APIRouter()

@router.patch("/updatecomment/{comment_id}", response_model=schemas.CommentResponse)
def update_comment_function(comment_id: int, comment_info: schemas.CommentModify, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user) ):

    comment: models.Comment | None = get_comment_by_comment_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code = 404, detail= "No existe el comentario solicitado")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No se encuentra autorizado a modificar este comentario")
    content_comment_validated = validate_content_comment(comment_info.content)
    schema_validated = schemas.CommentModify(content = content_comment_validated)
    
    comment_updated = modify_comment(db, comment, schema_validated)

    return comment_updated