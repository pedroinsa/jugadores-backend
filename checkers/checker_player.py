from fastapi import HTTPException
import re
import string
import schemas
from utils.checker_utils_func import validate_letters,validate_letters_spaces, validate_letters_spaces_dots_numbers, validate_numbers_season, validate_datetime_birth, capitalize_and_strip, check_white_spaces,field_validation, length_validator, validate_letters_spaces_dots



## checker player post
def check_player_post(player: schemas.PlayerPostData):
     #capitalize and strip 
     capitalize_fields = ("name", "last_name","country", "last_team")
     key_values = capitalize_and_strip(player,capitalize_fields)
     #checks white spaces in string
     separated_string_fields= ("name", "last_name", "position", "country", "last_team")
     check_white_spaces(key_values, separated_string_fields)

     #validates each field individually.

     validate_functions = {
        "name": validate_letters_spaces,
        "last_name": validate_letters_spaces,
        "birth_date": validate_datetime_birth,
        "position": validate_letters_spaces,
        "preferred_foot": validate_letters,
        "country":  validate_letters_spaces,
        "last_team": validate_letters_spaces_dots_numbers,
        "last_played_season": validate_numbers_season

       }     

     field_validation(key_values, validate_functions)
    #check max length and min length
     max_length_group = {
        "name": 30,
        "last_name": 30,
        "position": 25,
        "preferred_foot": 15,
        "country": 30,
        "last_team": 30,
        "last_played_season": 15
       }
     min_length_group ={
        "name": 3,
        "last_name": 3,
        "position": 5,
        "preferred_foot": 4,
        "country": 4,
        "last_team": 3,
        "last_played_season": 4
     }     
     length_validator(key_values,max_length_group,min_length_group)
     
     return schemas.PlayerPostData(**key_values)    
   
###checker player patch

def check_player_patch(player: schemas.PlayerUpdate):
       #capitalize and strip 
       capitalize_fields = ("name", "last_name", "country", "last_team", "other_nationality")
       key_values = capitalize_and_strip(player, capitalize_fields)
       #checks white spaces in string
       separated_string_fields= ("name", "last_name", "position", "country", "last_team", "other_nationality", "injury_description")
       check_white_spaces(key_values, separated_string_fields)

       #validates each field individually.
       validate_functions = {
        "name": validate_letters_spaces,
        "last_name": validate_letters_spaces,
        "birth_date": validate_datetime_birth,
        "position": validate_letters_spaces,
        "preferred_foot": validate_letters,
        "country":  validate_letters_spaces,
        "last_team": validate_letters_spaces_dots_numbers,
        "last_played_season": validate_numbers_season,
        "other_nationality": validate_letters_spaces,
        "injury_description": validate_letters_spaces_dots

       }     

       field_validation(key_values, validate_functions)

       #check max length and min length
       max_length_group = {
        "name": 30,
        "last_name": 30,
        "position": 25,
        "preferred_foot": 15,
        "country": 30,
        "last_team": 30,
        "last_played_season": 15,
        "other_nationality": 30,
        "injury_description": 300
       }
       min_length_group ={
        "name": 3,
        "last_name": 3,
        "position": 5,
        "preferred_foot": 4,
        "country": 4,
        "last_team": 3,
        "last_played_season": 4,
        "other_nationality": 4,
        "injury_description": 5
     } 
       length_validator(key_values,max_length_group,min_length_group)
       return schemas.PlayerUpdate(**key_values) 


     
     

 
     

