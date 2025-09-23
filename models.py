from database import Base
from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey,Date, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone




class User(Base):
     __tablename__ = 'users'
     id = Column(Integer, primary_key= True, index= True)
     username = Column(String(25), unique= True, index=True)
     email  = Column (String, unique =True, index = True)
     password = Column(String)
     role = Column(Enum("user", "admin", "superadmin",name = "user_roles"), default="user")
     created_player = Column(Boolean, default=False)
     created_at = Column(Date, default = datetime.now(timezone.utc))
     is_active = Column(Boolean, default=True)
     deactivated_by_some_manager = Column(Boolean, default = False)
     
     player = relationship("Player",back_populates="user", uselist=False )
     comments = relationship("Comment", back_populates="user")
     likes = relationship("Like", back_populates="user")



class Player(Base):
     __tablename__ = "players"
     id = Column(Integer, primary_key=True, index = True)
     user_id = Column(Integer,ForeignKey("users.id"))
     name = Column(String(30))
     last_name = Column(String(30))
     birth_date = Column(Date)
     position = Column(String(25))
     preferred_foot = Column(String(15))
     height = Column(Integer, nullable=True)
     weight = Column(Integer, nullable= True)
     goals_scored = Column(Integer, nullable = True)
     country = Column(String(30)) 
     other_nationality = Column(String(30),nullable=True)
     last_team = Column(String(30))
     last_played_season = Column(String(15))
     current_injury = Column(Boolean, default=False)
     injury_description = Column(String(300), nullable=True)
     international_experience = Column(Boolean, default=False)
     image_url = Column(String, nullable=True)
     user = relationship("User", back_populates="player", uselist=False)
     player_career = relationship("Player_career", back_populates="player", cascade="all, delete-orphan")
     posts = relationship("Post", back_populates="player", cascade="all, delete")

class Player_career(Base):
     __tablename__ = "player_career"
     id = Column(Integer, primary_key= True, index = True) 
     player_id = Column(Integer, ForeignKey("players.id"))    
     team = Column(String(30))
     date_start = Column(Date)
     date_end = Column(Date)
     

     player = relationship("Player", back_populates="player_career") 



class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key= True, index = True)
    player_id = Column(Integer, ForeignKey("players.id"))
    content =  Column(String)
    media_url = Column(String)
    created_at = Column(Date, default = datetime.now(timezone.utc))
    player = relationship("Player", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
    likes = relationship("Like", back_populates="post", cascade="all, delete")

class Comment(Base):
     __tablename__ = "comments"
     id = Column(Integer, primary_key= True, index= True) 
     post_id = Column(Integer, ForeignKey("posts.id"))
     user_id  = Column(Integer, ForeignKey("users.id"))
     content = Column(String)
     created_at = Column(Date, default = datetime.now(timezone.utc))
     post = relationship("Post", back_populates="comments")
     user = relationship("User", back_populates="comments")
class Like (Base):
     __tablename__ = "likes"
     id =Column(Integer, primary_key=True, index= True)
     post_id = Column(Integer, ForeignKey("posts.id"))
     user_id = Column(Integer, ForeignKey("users.id"))
     created_at = Column(Date, default = datetime.now(timezone.utc))
     post = relationship("Post", back_populates="likes")
     user = relationship("User", back_populates="likes")

