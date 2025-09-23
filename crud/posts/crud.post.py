from sqlalchemy.orm import Session
from models import Post
import schemas

#create post
def create_post(db: Session, post: schemas.PostCreate, player_id: int ):
    new_post = Post(content= post.content, media_url = post.media_url, player_id = player_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
