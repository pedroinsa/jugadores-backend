from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud.player_career.crud_post import create_player_career
import schemas
import models
from typing import List
from checkers.checker_player_career import player_career_post
from utils.utils import get_current_user

router = APIRouter()


@router.post("/player_career")
def create_player_career_function (player_career_info: schemas.PlayerCareerBase, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
  
  if current_user.created_player == False:
        raise HTTPException(status_code=400, detail="El usuario no ha creado ningún jugador todavía")
  player: models.Player | None =  current_user.player
  if not player :
        raise HTTPException(status_code=404, detail="El jugador no existe en la base de datos")
  player_id = player.id
  
  player_career_schema_checked = player_career_post(player_career_info, player_id, db )

  player_career_model = create_player_career(db, player_career_schema_checked, player_id)
  
   
  return player_career_model



