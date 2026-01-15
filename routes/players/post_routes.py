from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from utils.utils import get_current_user
from checkers.checker_player import check_player_post
from crud.players.crud_post import create_player, upload_profile_image_player
from crud.users.crud_patch import change_attribute_created_player
from crud.players.crud_get import get_player_by_id
import schemas
from models import User
from utils.mediafile import save_media

router = APIRouter()


@router.post("/create-player", response_model=schemas.PlayerData)
def create_player_route(player: schemas.PlayerPostData, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   
   if current_user.created_player:
       raise HTTPException(status_code=400, detail="El usuario ya ha creado un jugador") 
     
   player_checked = check_player_post(player)   

   new_player = create_player(db, player_checked, current_user.id)

   change_attribute_created_player(db=db, user=current_user, attribute_value=True)
     
   return new_player 

@router.post("/player/upload-image/{player_id}")
async def upload_image_function(player_id: int, media_file: UploadFile | None = File(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    player = get_player_by_id(db, player_id)  
    if not player:
        raise HTTPException(status_code=404, detail="El jugador solicitado no existe")  
    if not current_user.created_player:
        raise HTTPException(status_code=400, detail="El usuario actual no tiene un jugador asociado") 
    if player.user_id != current_user.id:
        raise HTTPException(status_code=403, detail= "No se encuentra autorizado a modificar este jugador") 
    media_url = None
    if media_file:
        media_url = await save_media(media_file, "player_profile")

    player_updated = upload_profile_image_player(db, player, media_url)    

    return player_updated
    

