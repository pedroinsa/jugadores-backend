from sqlalchemy.orm import Session
from models import Player_career
import schemas


#returns all player career from player
def get_all_player_career(db: Session, player_id: int):
    return db.query(Player_career).filter(Player_career.player_id == player_id).all()

#return all player career by team
def get_all_player_career_by_team(db:Session, team: str, skip: int = 0, limit: int = 20):
    return db.query(Player_career).filter(Player_career.team == team).offset(skip).limit(limit).all()

#returns player career by id
def get_player_career(db: Session, player_career_id: int):
    return db.query(Player_career).filter(Player_career.id == player_career_id).first()




