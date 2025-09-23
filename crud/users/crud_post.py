from sqlalchemy.orm import Session
import models
import schemas

#create user
def create_user(db: Session, user: schemas.UserPostData ):
    new_user =  models.User(username = user.username, email = user.email, password = user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
#create user for tests
def create_user_for_tests(db: Session, user: schemas.UserPostDataTests ):
    new_user =  models.User(username = user.username, email = user.email, password = user.password, role = user.role, is_active = user.is_active, deactivated_by_some_manager = user.deactivated_by_some_manager  )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user