from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from utils.utils import get_current_user
from checkers.checker_player import check_player_post
from crud.players.crud_post import create_player
from crud.users.crud_patch import change_attribute_created_player
import schemas
from models import User

router = APIRouter()


@router.post("/create-player", response_model=schemas.PlayerData)
def create_player_route(player: schemas.PlayerPostData, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   
   if current_user.created_player:
       raise HTTPException(status_code=400, detail="El usuario ya ha creado un jugador") 
     
   player_checked = check_player_post(player)   

   new_player = create_player(db, player_checked, current_user.id)

   change_attribute_created_player(db=db, user=current_user, attribute_value=True)
     
   return new_player 



    

