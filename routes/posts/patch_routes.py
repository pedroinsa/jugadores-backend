from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from utils.utils import get_current_user
import schemas
import models
from typing import List, Optional
from utils.mediafile import save_media
from crud.posts.crud_get import get_post_by_post_id
from crud.posts.crud_patch import modify_post
from utils.mediafile import save_media
from checkers.checker_posts import validate_content_post


router = APIRouter()

@router.patch("/updatepost/{post_id}", response_model= schemas.PostResponseSimple)
async def update_post_function(post_id: int, content: str | None = Form(None), media_file: UploadFile | None = File(None),
                          remove_media: bool = False,
                          db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    player: models.Player = current_user.player
    if not player:
        raise HTTPException(status_code=404, detail=("No hay jugador asociado a este usuario"))
    post = get_post_by_post_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="No existe el post solicitado")
    if post.player_id != player.id:
        raise HTTPException(status_code=403, detail="No está autorizado a modificar este post")
    content_validate = content
    if content is not None:
        content_validate  = validate_content_post(content)
        
    media_url = None
    if media_file is not None:
        media_url = await save_media(media_file, "post")

    post_updated = modify_post(db,post,content_validate,media_url,remove_media) 

    return post_updated
    

   
   
    