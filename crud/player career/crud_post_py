from sqlalchemy.orm import Session
from models import Player_career
import schemas

#create player career
def create_player_career(db: Session, player_career: schemas.PlayerCareerBase, player_id: int):
    new_player_career = Player_career(player_id = player_id)
    player_career_dict = player_career.model_dump(exclude_unset= True)
    for key, value in player_career_dict.items():
        setattr(new_player_career, key,value)
    db.add(new_player_career)   
    db.commit()
    db.refresh(new_player_career) 
    return new_player_career 
      