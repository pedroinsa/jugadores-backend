from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from typing import List
from utils.utils import get_current_user
from crud.posts.crud_get import get_post_by_post_id
from crud.likes.crud_post import create_like



router = APIRouter()

@router.post("/createlike/{post_id}")
def create_like_function(post_id: int, db:Session= Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user_id = current_user.id
    post = get_post_by_post_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="El post solicitado no existe")
    like = create_like(db, post_id, user_id)

    return like
    
    
