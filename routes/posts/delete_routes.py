from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from typing import List
from utils.utils import get_current_user
from crud.posts.crud_get import get_post_by_post_id
from crud.posts.crud_delete import delete_post

router = APIRouter()


@router.delete("/deletepost/{post_id}")
def delete_post_function(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    player: models.Player = current_user.player
    if not player:
        raise HTTPException(status_code=404, detail="No existe jugador asociado a este usuario")
    post = get_post_by_post_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="No existe el post solicitado")
    if post.player_id != player.id:
        raise HTTPException(status_code=403, detail="No está autorizado a eliminar este post")
    
    return delete_post(db,post)
    