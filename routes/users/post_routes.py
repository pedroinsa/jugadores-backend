from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from crud.users.crud_get import get_user_by_username, get_user_by_email
from crud.users.crud_post import create_user
from utils.utils import generate_token
import checkers.checkers as checkers
from database import get_db
from utils.utils import get_cookies
import schemas
from sqlalchemy.orm import Session
import bcrypt
import models
from datetime import datetime, timedelta, timezone
from jose import jwt
import re
from env import TOKEN_DURATION



router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse, status_code= 201)
def user_register(request: Request,user: schemas.UserPostData, db: Session = Depends(get_db) ):
    if get_cookies(request):
         raise HTTPException(status_code=400, detail="Ya hay una sesión activa, no puedes registrarte")
    username = checkers.check_username (user.username)
    email = checkers.check_email(user.email)
    password = checkers.check_password(user.password)

    user = get_user_by_username(db, username=username)  
    user_email = get_user_by_email(db, email=email)

    if user or user_email:
        raise HTTPException(status_code=400, detail = "El usuario o email ya se han registrado antes")
    
    password_hashed = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
    new_user_schema = schemas.UserPostData(username=username, email=email, password= password_hashed.decode("utf-8"))
    new_user =  create_user(db,new_user_schema)

    access_token = {"sub": new_user.username, "exp": datetime.utcnow() + timedelta(seconds = TOKEN_DURATION) }

    token = generate_token(access_token)

    response = JSONResponse(content={"msg": "el usuario se ha registrado"},status_code=201)
    response.set_cookie(key = "access_token", value = token, httponly=True, secure=True,samesite="strict", max_age=TOKEN_DURATION)
    
    return response


@router.post("/login")
def user_login(request: Request,user: schemas.UserLoginData, db: Session= Depends(get_db)):
   
  
     if get_cookies(request):
         raise HTTPException(status_code=400, detail="Ya hay una sesión activa")
     if re.match(r'^[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚüÜ._%+-]+@[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚüÜ.-]+\.[a-zA-Z]{2,}$', user.user_credential):
         user_credential = checkers.check_email(user.user_credential)
         user_db = get_user_by_email(db, email=user_credential) 

     else:
         user_credential = checkers.check_username(user.user_credential)
         user_db = get_user_by_username(db, username=user_credential)
     
     if not user_db :
            raise HTTPException(status_code=404, detail="El usuario no existe en los registros")
     
     if not bcrypt.checkpw(user.password.encode("utf-8"), user_db.password.encode("utf-8")):
            raise HTTPException(status_code=400, detail= "La contraseña no coincide")

     access_token = {"sub": user_db.username, "exp": datetime.utcnow() + timedelta(seconds = TOKEN_DURATION) }

     token = generate_token(access_token)

     response = JSONResponse(content={"msg": "Login realizado con éxito"})
     response.set_cookie(key = "access_token", value = token, httponly=True, secure=True,samesite="strict", max_age=TOKEN_DURATION)
    
     return response


@router.post("/logout")
def user_logout (request: Request):
     if not get_cookies(request):
          raise HTTPException(status_code=400, detail="No hay sesión activa")
     
     response = JSONResponse(content={"msg": "Logout realizado con éxito"})
     response.set_cookie(key = "access_token", value="invalid_token", httponly=True, secure= True, samesite="strict", max_age=0, expires=datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(seconds=10))
     return response