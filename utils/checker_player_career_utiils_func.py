from utils.checker_player_utils_func import enhanced_capitalizer, validate_letters_spaces_dots_numbers
from fastapi import HTTPException
from datetime import datetime, date
from sqlalchemy.orm import Session
import schemas
from models import Player_career
import re

#validates String
def validate_string_team(field: str, team: str):
    if not team:
        raise HTTPException(status_code=400, detail="No se ha brindado el nombre del equipo")
    if len(team) < 3:
        raise HTTPException(status_code=400, detail="El equipo debe contener más de 3 caracteres")
    if len(team) > 50:
        raise HTTPException(status_code=400, detail= "El equipo debe no puede contener más de 50 caracteres")
    validate_letters_spaces_dots_numbers(field, team)
    team_checked = enhanced_capitalizer(team)

    return team_checked

#validates dates
def validate_dates(date_start: date, date_end: date):
    today = date.today()
    MAX_YEARS_AGO = 25
    if not date_start:
        raise HTTPException(status_code=400, detail="La fecha de ingreso es obligatoria")
    if not date_end:
         raise HTTPException(status_code=400, detail="La fecha de egreso es obligatoria")
    if date_end < date_start:
            raise HTTPException(status_code=400, detail="La fecha de egreso no puede ser anterior a la de ingreso")
    if date_start > today:
        raise HTTPException(status_code=400, detail="La fecha de ingreso no puede ser futura")
    if date_end > today:
            raise HTTPException(status_code=400,detail= "La fecha de egreso no puede ser futura")
    limit_date = today.replace(year=(today.year-MAX_YEARS_AGO))
    if date_start < limit_date:
        raise HTTPException( status_code=400, detail= f"La fecha de ingreso no puede ser mayor a {MAX_YEARS_AGO} años")
    
#validates that there are no duplicate 'player_career' entries.”    
    
def validate_duplicate_career_create(db: Session, player_id: int, team: str, date_start: date, date_end: date):
    found = db.query(Player_career).filter(
        Player_career.player_id == player_id,
        Player_career.team.ilike(team),
        Player_career.date_start == date_start,
        Player_career.date_end == date_end
    ).first()
    if found:
        raise HTTPException(400, f"Ya existe un registro idéntico para {team} en esas fechas.")    

def validate_duplicate_career_update(db: Session, player_id: int, player_career_id: int, team: str, date_start: date, date_end: date ):
     found = db.query(Player_career).filter(
          Player_career.player_id == player_id,
          Player_career.team.ilike(team),
          Player_career.date_start == date_start,
          Player_career.date_end == date_end,
          Player_career.id != player_career_id
     ).first()
     if found:
        raise HTTPException(400, f"Ya existe un registro idéntico para {team} en esas fechas.")  

def validate_overlap_career(db: Session, player_id: int, new_start: date, new_end: date | None):
    MAX_DIFFERENCE = 60
    careers = db.query(Player_career).filter(Player_career.player_id == player_id).all()
    for career in careers:
        overlap_days = get_overlap_days_difference(career.date_start, career.date_end, new_start, new_end)
        if overlap_days > MAX_DIFFERENCE:  
            raise HTTPException(status_code=400 ,detail=f"Las fechas se superponen con su paso por {career.team}."
            )

def validate_overlap_career_update(db: Session, player_id: int, player_career_id: int, new_start: date, new_end: date):
    MAX_DIFFERENCE = 60
    careers = db.query(Player_career).filter(Player_career.player_id == player_id, Player_career.id != player_career_id).all()
    for career in careers:
        overlap_days = get_overlap_days_difference(career.date_start, career.date_end, new_start, new_end)
        if overlap_days > MAX_DIFFERENCE:  
            raise HTTPException(status_code=400 ,detail=f"Las fechas se superponen con su paso por {career.team}."
            )


def get_overlap_days_difference(career_db_start, career_db_end, new_career_start, new_career_end):
    latest_start = max(career_db_start, new_career_start)
    earliest_end = min(career_db_end, new_career_end)
    difference_between = (earliest_end - latest_start).days
    return max(0, difference_between)    