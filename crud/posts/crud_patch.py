from sqlalchemy.orm import Session
from models import Post
import schemas


# modify post
def modify_post(db: Session, post: Post, post_update: schemas.PostModify):
         
    updating_post = post_update.model_dump(exclude_unset=True)
    for key,value in updating_post.items():
        setattr(post,key,value)
    db.commit()
    db.refresh(post)
    return post