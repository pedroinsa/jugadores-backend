from sqlalchemy.orm import Session, joinedload
from models import Post

#returns all posts from user
def get_all_posts_by_player(db: Session, player_id: int, skip: int = 0, limit: int = 20 ):

    return db.query(Post).filter(Post.player_id == player_id).order_by(Post.id.desc()).offset(skip).limit(limit).all()

#returns all posts that match the content search
def get_posts_by_content(db: Session, content: str, skip: int = 0, limit: int = 20):

    return db.query(Post).options(joinedload(Post.player)).filter(Post.content.ilike(f"%{content}%")).order_by(Post.id.desc()).offset(skip).limit(limit).all()

#return post by post_id

def get_post_by_post_id(db: Session, post_id: int):
    return db.query(Post).options(joinedload(Post.player)).filter(Post.id == post_id).first()