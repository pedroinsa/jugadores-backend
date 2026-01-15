from sqlalchemy.orm import Session
import models
import schemas

#create player
def create_player(db: Session, player: schemas.PlayerPostData, user_id: int ):
    player_dict = player.model_dump()
    valid_fields_in_model = {col.name for col in models.Player.__table__.columns}
    player_data =  { key:value for key,value in player_dict.items() if key in valid_fields_in_model}
    player_data['user_id'] = user_id
    new_player = models.Player(**player_data)

    db.add(new_player) 
    db.commit()
    db.refresh(new_player)
    return new_player

#upload profile image
def upload_profile_image_player(db: Session, player: models.Player, media_url: str | None):
    player.image_url = media_url
    db.commit()
    db.refresh(player)
    return player

