from typing import Optional, List, Literal
from pydantic import BaseModel, Field, model_validator,field_validator, EmailStr, ConfigDict
from datetime import datetime, date

### users  

class UserPostData(BaseModel):
      username: str
      email: str
      password: str
class UserPostDataTests(BaseModel):
     username: str
     email: str
     password: str
     role: Literal ["user", "admin", "superadmin"] = "user"
     is_active: bool
     deactivated_by_some_manager: bool


class UserLoginData(BaseModel) :
      user_credential: str
      password: str    

class UserResponse(BaseModel):
      username: str
      email: str
      id: int
      created_at : datetime
      role: Literal ["user", "admin", "superadmin"] = "user"
      is_active: bool
      
      model_config = ConfigDict(from_attributes=True)

class UserUpdatePassword(BaseModel):
      current_password : str 
      new_password : str 

class UserUpdateActiveStatus(BaseModel):
      is_active: bool
     
class UserChangeRole (BaseModel):
     new_role : Literal ["user", "admin", "superadmin"]

###player career

class PlayerCareerBase(BaseModel):
    team: str
    date_start: Optional[date] = None
    date_end: Optional[date] = None


class PlayerCareer(PlayerCareerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class PlayerCareerUpdate(BaseModel):
     team: Optional[str]
     date_start : Optional[date]
     date_end :Optional[date] 
### Players
class PlayerData(BaseModel):
      id : int
      user_id : int
      name : str = Field(..., max_length= 30)
      last_name : str = Field(..., max_length=30)  
      birth_date : date
      position: str = Field(..., max_length=25)
      preferred_foot: str = Field(..., max_length=15)
      height: Optional[int] = Field(None, ge = 140, le= 240)
      weight: Optional[int] = Field(None, ge= 40, le= 150)
      goals_scored : Optional[int] = None
      country : str = Field(..., max_length= 30)
      other_nationality: Optional[str] = Field(default= None,max_length=25)
      player_career : List[PlayerCareer] = []
      # career : List[str] = Field(default_factory=list)
      last_team : str = Field(..., max_length=30)
      last_played_season: str = Field(..., max_length=15)
      current_injury: bool = False
      injury_description : Optional[str] = None
      international_experience: bool = False
      image_url : Optional[str] = None

class PlayerPostData (BaseModel): 
      name : str 
      last_name : str 
      birth_date: date
      position: str 
      preferred_foot: str 
      country : str 
      last_team : str
      last_played_season: str

      model_config = ConfigDict(from_attributes=True)


class PlayerUpdate (BaseModel):
      name : Optional[str] = Field(None, min_length=3, max_length= 30)
      last_name : Optional[str] = Field(None,min_length=3, max_length=30)  
      birth_date : Optional[date] = None
      position: Optional[str] = Field(None, min_length=5, max_length=25)
      preferred_foot: Optional[str] = Field(None,min_length=4, max_length=15)
      height: Optional[int] = Field(None, ge = 140, le= 240)
      weight: Optional[int] = Field(None, ge= 40, le= 150)
      goals_scored : Optional[int] = None
      country : Optional[str] = Field(None,min_length=4, max_length= 30)
      other_nationality: Optional[str] = Field(None,min_length=4, max_length=30)
      player_career : Optional[List[PlayerCareer]] = None
      # career : Optional[List[str]] = Field(default_factory=list)
      last_team : Optional[str]= Field(None, min_length=3, max_length=30)
      last_played_season: Optional[str] = Field(None, min_length=4,max_length=15)
      current_injury: Optional[bool] = False
      injury_description : Optional[str] = Field(None, max_length=300)
      international_experience: Optional[bool] = False
      image_url : Optional[str] = None
     
      model_config = ConfigDict(from_attributes=True)

      @field_validator("name", "last_name", "birth_date", "position", "preferred_foot","country", 
                       "last_team", "last_played_season", mode="before")
      def validate_required_fields(cls, value, ):
           if value is None:
                raise ValueError("field is required")   
           return value  
            




### Post

class PostCreate(BaseModel):
     content : str = Field(..., min_length= 5, max_length=300)
     media_url: Optional[str] = None

class PostResponse(PostCreate):
      id: int
      player_id : int  
      created_at :  datetime     
      comments : Optional[List[str]] = []
      likes : Optional[int]
      player: PlayerData

      model_config = ConfigDict(from_attributes=True)

class PostModify(BaseModel):
     content: Optional[str] = Field(..., min_length= 5, max_length=300)
     media_url : Optional[str]

###Comments
class CommentCreate(BaseModel):
     content : str = Field(..., min_length=1,max_length=250)

class CommentResponse(BaseModel) :
     id: int 
     post_id: int
     user_id : int
     content: str = Field(min_length=1,max_length=250)
     created_at: datetime
     user: UserResponse

     model_config = ConfigDict(from_attributes=True)

class CommentModify(BaseModel):
     content: str = Field(min_length=1,max_length=250)


###Likes

class LikeResponse(BaseModel):
     id: int
     post_id: int
     user_id: int
     created_at: datetime
