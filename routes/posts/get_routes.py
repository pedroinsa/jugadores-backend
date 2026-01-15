from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from typing import List
from crud.posts.crud_get import get_all_posts_by_player
from crud.players.crud_get import get_player_by_id
from utils.utils import get_current_user


router = APIRouter()


@router.get("/posts/player/{player_id}/values",)
def get_posts_from_player(player_id: int,skip: int = 0, limit: int = 20,  db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user) ):
    player = current_user.player
    if not player:
        raise HTTPException(status_code=404, detail= "No hay jugador asociado con este usuario")
    player_search = get_player_by_id(db, player_id)
    if not player_search:
        raise HTTPException(status_code=404, detail="No existe el jugador buscado")
    posts = get_all_posts_by_player(db, player_id, skip, limit)
    #if not posts:
    #    raise HTTPException(status_code=404, detail="No se han encontrado posts asociados a este jugador")
    
    return posts

