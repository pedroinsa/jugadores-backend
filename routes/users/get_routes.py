from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud.users.crud_get  as crud
from database import get_db
import schemas
from typing import List


router = APIRouter()

#returns all users, both active and inactive."
@router.get("/users", response_model=List[schemas.UserResponse])
def get_users (skip: int = 0 , limit: int = 20, db: Session = Depends(get_db)):
       users = crud.get_all_users(db, skip = skip , limit = limit)
       return users
#returns only active users
@router.get("/users/actives", response_model=List[schemas.UserResponse])
def get_users_actives(skip: int = 0, limit: int =20, db: Session = Depends(get_db)):
       users =  crud.get_all_users_actives(db, skip = skip , limit = limit)
       return users
#searches all matches that match the 'username' string.
@router.get("/users/username", response_model=List[schemas.UserResponse])
def get_users (username: str, skip: int = 0, limit: int= 20, db: Session = Depends(get_db)):
       users = crud.get_users_by_username(db, username, skip=skip, limit =limit)
       return users 
#searches all matches that match the 'email" string
@router.get("/users/email", response_model=List[schemas.UserResponse])
def get_users (email: str, skip: int = 0, limit: int= 20, db: Session = Depends(get_db)):
       users = crud.get_users_by_email(db, email, skip=skip, limit =limit)
       return users 

#returns a user by exact username
@router.get("/user/username", response_model=schemas.UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):
       user = crud.get_user_by_username(db, username)
       if not user:
              raise HTTPException(status_code=404, detail="No existe un usuario con ese username")
       return user
#returns a user by email
@router.get("/user/email", response_model=schemas.UserResponse)
def get_user(email: str, db: Session = Depends(get_db)):
       user = crud.get_user_by_email(db, email)
       if not user:
              raise HTTPException(status_code=404, detail="No existe un usuario con ese email")
       return user

#returns a user by id
@router.get("/user/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
       user = crud.get_user_by_id(db, id)
       if not user:
              raise HTTPException(status_code=404, detail="No existe un usuario con ese ID")
       return user 
