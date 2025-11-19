from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from utils.utils import get_current_user
from crud.players.crud_get import get_player_by_user_id
from crud.players.crud_patch import update_player
from checkers.checker_player import check_player_patch
import schemas
import models


router = APIRouter()


@router.patch("/update-player")
def update_player_route(player_info: schemas.PlayerUpdate, db: Session = Depends(get_db), current_user: models.User=Depends(get_current_user) ):
    if current_user.created_player == False:
        raise HTTPException(status_code=400, detail="El usuario no ha creado ningún jugador todavía")
    player =  current_user.player
    if not player :
        raise HTTPException(status_code=404, detail="El jugador no existe en la base de datos")
    player_checked = check_player_patch(player_info)
    
    player_updated = update_player(db, player, player_checked)
    

    return player_updated
    
   