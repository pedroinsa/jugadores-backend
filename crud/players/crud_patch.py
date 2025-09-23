from sqlalchemy.orm import Session
import models
import schemas


#update player
def update_player (db:Session, player: models.Player, player_information: schemas.PlayerUpdate):
    


    updating_player = player_information.model_dump(exclude_unset=True)
    valid_fields = {col.name for col in models.Player.__table__.columns}
    for key,value in updating_player.items():
       if key in valid_fields:  
         setattr(player,key,value) 
    db.commit()
    db.refresh(player) 

    return player   

  