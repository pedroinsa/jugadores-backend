from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from typing import List
from utils.utils import get_current_user
from crud.likes.crud_delete import delete_like
from crud.likes.crud_get import get_like_by_like_id



router = APIRouter()

@router.delete("/deletelike/{like_id}")
def delete_like_function(like_id: int, db:Session= Depends(get_db), current_user: models.User = Depends(get_current_user)):

    like = get_like_by_like_id(db, like_id)
    if not like:
       raise HTTPException(status_code=404, detail="No existe el like solicitado")
    if like.user_id != current_user.id:
       raise HTTPException(status_code=403, detail="No está autorizado a eliminar este like")
    
    return delete_like(db,like)

    

