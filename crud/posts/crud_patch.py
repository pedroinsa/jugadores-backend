from sqlalchemy.orm import Session
from models import Post
import schemas


# modify post
def modify_post(db: Session, post: Post, content: str | None = None, media_url: str | None = None, remove_media: bool = False):

    if content is not None:
        post.content = content
    if remove_media:
        post.media_url = None
    elif media_url is not None:
        post.media_url = media_url
                 
    db.commit()
    db.refresh(post)
    return post