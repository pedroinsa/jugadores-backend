from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud.players.crud_get import get_player_by_id
from crud.players.crud_delete import delete_player
from utils.utils import get_current_user
import schemas
import models

router = APIRouter()

@router.delete("/player/${id}")
def delete_player_selected(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user) ):
      player = get_player_by_id(db, id)
      if not player:
            raise HTTPException(status_code=404, detail="El jugador no existe")
      if player.user_id != current_user.id :
            raise HTTPException(status_code=403, detail= "No se encuentra autorizado a eliminar este jugador")
   
      delete_player(db, current_user, player)
      return {"msg": "el jugador ha sido eliminado"}