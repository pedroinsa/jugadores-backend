from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from crud.players.crud_get import get_all_players, get_all_player_by_last_name, get_all_players_match_last_name, get_all_player_by_position, get_all_player_by_country, get_player_by_id
import schemas



router = APIRouter()

#returns all players
@router.get("/players", response_model=List[schemas.PlayerData])
def get_players(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    players = get_all_players(db, skip=skip, limit=limit)
    return players

#returns all players that match the last name str
@router.get("/players/last-name-matches")
def get_players_by_last_name(last_name: str, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    players = get_all_players_match_last_name(db, last_name, skip = skip , limit = limit)
    return players
#returns all player the match the last name(last_name exactly)
@router.get("/players/last-name")
def get_players_by_last_name(last_name: str, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    players = get_all_player_by_last_name(db, last_name, skip = skip , limit = limit)
    return players
#returns players by position
@router.get("/players/position")
def get_players_by_position(position: str, skip: int = 0, limit: int = 20, db: Session= Depends(get_db)):
    players = get_all_player_by_position(db,position, skip = skip, limit = limit)
    return players
#returns players by country
@router.get("/players/country")
def get_players_by_country(country: str, skip: int = 0, limit: int = 20, db: Session=Depends(get_db)):
    players = get_all_player_by_country(db, country, skip = skip, limit = limit) 
    return players
#return player by id
@router.get("/player/{id}")
def get_player(id: int, db: Session = Depends(get_db)):
    player = get_player_by_id(db, id)
    if not player:
        raise HTTPException(status_code=404, detail="No se ha encontrado el jugador")
    return player
    