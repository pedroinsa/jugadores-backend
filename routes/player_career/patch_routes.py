from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from typing import List
from utils.utils import get_current_user
from crud.player_career.crud_get import get_player_career
from crud.player_career.crud_patch import modify_player_career
from checkers.checker_player_career import player_career_patch


router = APIRouter()

@router.patch("/player_career/{id}")
def update_player_career_function(id: int, player_career_inf: schemas.PlayerCareerUpdate, db: Session = Depends(get_db), current_user: models.User=Depends(get_current_user)):
    
     if current_user.created_player == False:
        raise HTTPException(status_code=400, detail="El usuario no ha creado ningún jugador todavía")
     player: models.Player | None =  current_user.player
     if not player :
        raise HTTPException(status_code=404, detail="El jugador no existe en la base de datos")
     #get player_career
     player_career = get_player_career(db = db, player_career_id= id)
     if not player_career:
         raise HTTPException(status_code=404, detail="El registro que busca no existe")
     #validates schema player_career and returns another schema
     player_career_schema_validated = player_career_patch(player_career,player_career_inf, player.id, db)
     #updates player_career in db
     player_career_model = modify_player_career(db, player_career, player_career_schema_validated)

     return player_career_model

     