from sqlalchemy.orm import Session
import models 

#update password
def update_password (db: Session, user: models.User, password):
    user.password = password
    db.commit()
    db.refresh(user)
    return  
#change user's status    
def change_user_status(db: Session, user: models.User, status: bool,deactivate_manager_bool = False):
    user.is_active = status
    user.deactivated_by_some_manager = deactivate_manager_bool
    db.commit()
    db.refresh(user)
    return 
#change user's role
def change_user_role(db: Session, user: models.User, role):
    
    user.role  = role
    db.commit()
    db.refresh(user)
    return
#change attribute 'created_player'
def change_attribute_created_player(db: Session, user: models.User, attribute_value):
    user.created_player =  attribute_value
    db.commit()
    db.refresh(user)
    return

