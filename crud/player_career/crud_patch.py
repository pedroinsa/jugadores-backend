from sqlalchemy.orm import Session
from models import Player_career
import schemas


#modify player career

def modify_player_career(db: Session, player_career: Player_career, career_update : schemas.PlayerCareerUpdate):
    career_update_dict = career_update.model_dump(exclude_unset=True)
    for key, value in career_update_dict.items():
        setattr(player_career, key, value)
    db.commit()
    db.refresh(player_career)    

    return player_career