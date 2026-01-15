from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from utils.utils import get_current_user
import schemas
import models
from typing import List
from utils.mediafile import save_media
from checkers.checker_posts import validate_content_post
from crud.posts.crud_post import create_post


router = APIRouter()


@router.post("/create_post")
async def create_post_function( content: str = Form(...),
    media_file: UploadFile | None = File(None), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
   
    player: models.Player = current_user.player
    if not player:
        raise HTTPException(status_code=404, detail=("No hay jugador asociado a este usuario"))
    media_url = None
    if media_file:
        media_url = await save_media(media_file, "post")
    
    content_validated = validate_content_post(content)
    post_create_schema = schemas.PostCreate(content=content_validated, media_url=media_url)

    created_post = create_post(db, post_create_schema, player.id )


    return created_post