from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import schemas

#delete player
def delete_player(db: Session, linked_user: models.User, player: models.Player ):
      
      db.delete(player)
      linked_user.created_player = False
      db.commit()
      db.refresh(linked_user)

      return 