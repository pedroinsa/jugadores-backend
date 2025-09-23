from sqlalchemy.orm import Session
from models import Like

#create like
def create_like(db: Session, post_id: int, user_id: int):
    new_like = Like(post_id= post_id, user_id = user_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like