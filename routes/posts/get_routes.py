from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
from typing import List
from crud.posts.crud_get import get_all_posts_by_player


router = APIRouter()


@router.get("/posts/player/{player_id}")
def get_posts_from_player(player_id: int, db: Session = Depends(get_db)):




    return

