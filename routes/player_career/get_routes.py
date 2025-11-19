from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud.player_career.crud_get import get_all_player_career, get_all_player_career_by_team
import schemas
from typing import List


router = APIRouter()



#returns all player career from player
@router.get("/player_career/player/{player_id}", response_model=List[schemas.PlayerCareer])
def get_player_career(player_id: int, db: Session = Depends(get_db)):
    player_career = get_all_player_career(db,player_id)
    return player_career



