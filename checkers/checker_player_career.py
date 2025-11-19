from fastapi import HTTPException
import re
import string
import schemas
import models
from sqlalchemy.orm import Session
from utils.checker_player_utils_func import enhanced_capitalizer, validate_letters_spaces_dots_numbers
from utils.checker_player_career_utiils_func import validate_string_team, validate_duplicate_career_create, validate_dates, validate_overlap_career, validate_overlap_career_update, validate_duplicate_career_update



def player_career_post(player_career_info: schemas.PlayerCareerBase,player_id: int, db: Session ):
     
     #validates Team string
    team = validate_string_team("team", player_career_info.team.strip())
    #validates date_start and date_end
    validate_dates(player_career_info.date_start, player_career_info.date_end)
    #validates there are no duplicate
    validate_duplicate_career_create(db,player_id, player_career_info.team, player_career_info.date_start, player_career_info.date_end)
    #validates there are no overlap between two player_career
    validate_overlap_career(db,player_id,player_career_info.date_start, player_career_info.date_end)

    new_player_career =  schemas.PlayerCareerBase (team = team, date_start= player_career_info.date_start, date_end= player_career_info.date_end)
    return new_player_career  
    
   
def player_career_patch(player_career: models.Player_career, player_career_info: schemas.PlayerCareerUpdate, player_id: int, db: Session):

     team = player_career_info.team or player_career.team 
     date_start = player_career_info.date_start or player_career.date_start    
     date_end = player_career_info.date_end or player_career.date_end 
     
     if player_career_info.team:
            #validates Team string
            team = validate_string_team("team", team.strip())

     if player_career_info.team or player_career_info.date_start or player_career_info.date_end:
            #validates date_start and date_end
            validate_dates(date_start, date_end)
            #validates there are no duplicate
            validate_duplicate_career_update(db, player_id , player_career.id, team, date_start, date_end)
            #validates there are no overlap between two player_career
            validate_overlap_career_update(db, player_id, player_career.id, date_start, date_end)

     update_fields =  {}
     if player_career_info.team is not None and (team != player_career.team):
           update_fields["team"] = team
     if player_career_info.date_start is not None and (date_start != player_career.date_start):
           update_fields["date_start"] = date_start
     if player_career_info.date_end is not None and (date_end != player_career.date_end):
           update_fields["date_end"] = date_end       

     return schemas.PlayerCareerUpdate(**update_fields)            


