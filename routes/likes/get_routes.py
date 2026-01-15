from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from typing import List
from utils.utils import get_current_user
from crud.posts.crud_get import get_post_by_post_id
from crud.likes.crud_get import get_all_likes_from_post, get_all_likes_from_user



router = APIRouter()


@router.get("/likes/post/{post_id}", response_model= List[schemas.LikeResponse])
def get_likes_function(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = get_post_by_post_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="El post solicitado no existe")
    likes = get_all_likes_from_post(db, post_id)
    
    return likes

@router.get("/likes/user}", response_model= List[schemas.LikeResponse])
def get_like_user_function(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user_id = current_user.id
    likes = get_all_likes_from_user(db, user_id)
    
    return likes