from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from typing import List
from utils.utils import get_current_user
from crud.comments.crud_get import get_comment_by_comment_id
from crud.comments.crud_delete import delete_comment


router = APIRouter()


@router.delete("/deletecomment/{comment_id}")
def delete_comment_function(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    
    comment = get_comment_by_comment_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="No existe el comentario solicitado")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No está autorizado a eliminar este comentario")
    
    return delete_comment(db, comment)