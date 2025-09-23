from sqlalchemy.orm import Session
from models  import Like



#delete like

def delete_like(db: Session, like: Like):

    db.delete(like)
    db.commit()
    return "Like eliminado"

    