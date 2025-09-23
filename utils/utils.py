from fastapi import Depends,HTTPException
from fastapi.requests import Request
from sqlalchemy.orm import Session
from crud.users.crud_get import get_user_by_username
from database import get_db
from jose import jwt, JWTError
from env import ALGORITHM, SECRET


#genera el token
def generate_token(payload: dict):
    token = jwt.encode(payload, SECRET, ALGORITHM)

    return token
#obtiene el "sub" del token
def get_subject_in_token (token: str ):
   try:  
     payload = jwt.decode(token, SECRET, [ALGORITHM])
     subject  =  payload.get("sub")
     if subject is None :
          raise HTTPException(status_code=404, detail=("Error en las credenciales"))
     return subject     
   except JWTError:
       raise HTTPException(status_code=401, detail=("Token inválido "))
#obtiene las cookies de la Request          
def get_cookies(request: Request):
    return request.cookies.get("access_token")
#integra todas las funciones anteriores (la obtencion de cookie y la decodificacion del token para obtener el User en db):
def get_user_from_credentials(request, db :Session):
       token = get_cookies(request) 
       if token is None :
          raise HTTPException(status_code=400, detail=("No se ha podido obtener un token"))
       subject = get_subject_in_token(token)  
       user =  get_user_by_username(db, subject)   
       
       return user
       
#obtiene la cookie, obtiene el sub del token y busca en db el User y lo devuelve    
def get_current_user (request: Request, db: Session = Depends(get_db) ):
    
      user = get_user_from_credentials(request, db)
      
      if not user :
          raise HTTPException(status_code=404, detail="No ha encontrado el usuario")     
      
      
      return user

#obtiene la cookie, obtiene el sub del token, busca en la db el User y si es admin devuelve el User
def get_current_admin (request: Request, db: Session = Depends(get_db)):

    user = get_user_from_credentials(request, db)
    if not user :
          raise HTTPException(status_code=404, detail="No se ha encontrado el usuario")     
        
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="No tiene autorización para ingresar")
    return user      

def get_current_superadmin(request: Request, db: Session = Depends(get_db)):
     
      user = get_user_from_credentials(request, db)

      if not user:
          raise HTTPException(status_code=404, detail="No se ha encontrado el usuario")
      
      if user.role != "superadmin":
          raise HTTPException(status_code=403, detail="No tiene autorización para ingresar")
      
      return user

def get_current_admin_or_superadmin(request: Request, db: Session = Depends(get_db)):
    
    user = get_user_from_credentials(request, db)

    if not user :
        raise HTTPException(status_code=404, detail="No se ha encontrado el usuario")
    
    if not user.role in ("admin","superadmin"):
        raise HTTPException(status_code=403, detail="No tiene autorización para ingresar" )
    
    return user

