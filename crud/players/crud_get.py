from sqlalchemy.orm import Session
from models import Player

#returns all players
def get_all_players(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Player).offset(skip).limit(limit).all()

#returns all players that match the last name
def get_all_players_match_last_name(db: Session, last_name: str, skip: int = 0, limit: int = 20):
    return db.query(Player).filter(Player.last_name.ilike(f"%{last_name}%")).offset(skip).limit(limit).all()

#returns all player that match the last name exactly
def get_all_player_by_last_name(db: Session, last_name: str, skip: int = 0, limit: int = 20):
    return db.query(Player).filter(Player.last_name == last_name).offset(skip).limit(limit).all()
#returns all players by position
def get_all_player_by_position(db: Session, position: str, skip: int = 0, limit: int = 20):
    return db.query(Player).filter(Player.position == position).offset(skip).limit(limit).all()
#returns all players by country/nationality
def get_all_player_by_country (db: Session, country: str, skip: int = 0, limit: int = 20):
    return db.query(Player).filter(Player.country == country).offset(skip).limit(limit).all()

#returns the player by  ID
def get_player_by_id(db: Session, id: int):
    return db.query(Player).filter(Player.id == id).first()  

#returns the player by user_id:
def get_player_by_user_id(db: Session, user_id: int):
    return db.query(Player).filter(Player.user_id == user_id).first()
