from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from utils.utils import get_current_user, get_current_admin, get_current_superadmin, get_current_admin_or_superadmin
from crud.users.crud_get import get_user_by_id
from crud.users.crud_patch import update_password, change_user_status, change_user_role
import checkers.checkers as checkers
import schemas
import models
import bcrypt

router = APIRouter()

@router.patch("/new-password",)
def change_password(data: schemas.UserUpdatePassword,
                     current_user: models.User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if not data.current_password:
          raise HTTPException(status_code=400, detail="Debe ingresar la contraseña actual")
    if not bcrypt.checkpw(data.current_password.encode("utf-8"), current_user.password.encode("utf-8") ) :
           raise HTTPException(status_code=400, detail="La contraseña que ha ingresado no coincide con la original")
    
    if data.current_password  == data.new_password:
          raise HTTPException(status_code=400, detail="La nueva contraseña no debe ser igual a la original")
    new_password_checked = checkers.check_password(data.new_password)

    hashed_password = bcrypt.hashpw(new_password_checked.encode("utf-8"), bcrypt.gensalt())

    user_update = update_password(db,current_user, hashed_password.decode("utf-8"))

    return {"msg": "La contraseña se ha modificado con éxito"}

@router.patch("/user/deactivate")
def deactivate_user(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
      if not current_user.is_active:
            raise HTTPException(status_code=400, detail=("El usuario ya está desactivado"))
      
      change_user_status(db, current_user, status = False )
      
      return {"msg": "El usuario se ha desactivado"}

@router.patch("/user/reactivate") 
def reactivate_user (current_user : models.User = Depends(get_current_user), db: Session = Depends(get_db)):
       if current_user.is_active :
             raise HTTPException(status_code=400, detail="El usuario ya se encuentra activado")
       if current_user.deactivated_by_some_manager:
            raise HTTPException(status_code=403, detail="Un adminstrador lo ha desactivado. Para reactivar debe comunicarse con gerencia")
       change_user_status(db, current_user, status= True)

       return {"msg": "El usuario se ha activado"}


@router.patch("/admin/users/{id}/deactivate")
def deactivate_user (id: int, current_admin: models.User = Depends(get_current_admin), db: Session = Depends(get_db)):
      if current_admin.deactivated_by_some_manager:
            raise HTTPException(status_code=403, detail="Un superadmin te ha desactivado. Por favor comunicarse con gerencia")
      
      user = get_user_by_id(db, id)
     
      if not user :
            raise HTTPException(status_code=404, detail=("El usuario no se encuentra registrado"))
      if user.id == current_admin.id:
            raise HTTPException(status_code=403, detail="El admin no puede modificarse a sí mismo desde esta ruta")     
      if user.role == "admin" :
            raise HTTPException(status_code=403, detail="No tiene autorización para modificar otro admin")
      if user.role == "superadmin":
            raise HTTPException(status_code=403, detail="No tiene autorización para modificar un superadmin" )
      if not user.is_active:
            raise HTTPException(status_code=400, detail="El usuario ya está desactivado")
    
      change_user_status(db,user, status = False, deactivate_manager_bool = True)
      return {"msg": "El usuario se ha desactivado"}

@router.patch("/admin/users/{id}/reactivate")
def reactivate_user (id: int, current_admin: models.User = Depends(get_current_admin), db: Session = Depends(get_db)):
      if current_admin.deactivated_by_some_manager:
            raise HTTPException(status_code=403, detail="Un superadmin te ha desactivado. Por favor comunicarse con gerencia")

      user = get_user_by_id(db, id)
      if not user:
            raise HTTPException(status_code=404, detail="El usuario no se encuentra registrado")
      if user.id == current_admin.id:
            raise HTTPException(status_code=403, detail="El admin no puede modificarse a sí mismo desde esta ruta")
         
      if user.role == "admin":
            raise HTTPException(status_code=403, detail="No tiene autorización para modificar otro admin")
      if user.role == "superadmin":
            raise HTTPException(status_code=403, detail="No tiene autorización para modificar un superadmin")
      if user.is_active :
            raise HTTPException (status_code=400, detail="El usuario ya se encuentra activado")   
    
      change_user_status(db, user, status = True)
      return  {"msg": "El usuario se ha activado"}
          

@router.patch("/superadmin/users/{id}/deactivate")
def deactivate_user (id: int, current_superadmin: models.User = Depends(get_current_superadmin), db: Session = Depends(get_db)):
      user = get_user_by_id(db, id)
      if not user :
            raise HTTPException(status_code=404, detail=("El usuario no se encuentra registrado"))
      if user.id == current_superadmin.id:
            raise HTTPException(status_code=403, detail="El superadmin no puede modificarse a sí mismo desde esta ruta")

      if user.role == "superadmin":
            raise HTTPException(status_code=403, detail="No tiene autorización para modificar otro superadmin")
      if not user.is_active:
            raise HTTPException(status_code=400, detail="El usuario ya está desactivado")   
      
      change_user_status(db,user, status = False, deactivate_manager_bool = True )
      return {"msg": "El usuario se ha desactivado"}      

@router.patch("/superadmin/users/{id}/reactivate")
def reactivate_user (id: int, current_superadmin: models.User = Depends(get_current_superadmin), db: Session = Depends(get_db)):
      user = get_user_by_id(db, id)
      if not user:
            raise HTTPException(status_code=404, detail="El usuario no se encuentra registrado")
      if user.id == current_superadmin.id:
            raise HTTPException(status_code=403, detail="El superadmin no puede modificarse a sí mismo desde esta ruta")
         
      if user.role == "superadmin":
            raise HTTPException(status_code=403, detail="No tiene autorización para modificar otro superadmin")
      
      if user.is_active :
            raise HTTPException (status_code=400, detail="El usuario ya se encuentra activado")  

      change_user_status(db, user, status = True) 
   
      return  {"msg": "El usuario se ha activado"}

@router.patch("/manager/users/{id}/change-role")
def change_role_function(id: int, data: schemas.UserChangeRole, current_admin_superadmin: models.User = Depends(get_current_admin_or_superadmin), 
                     db: Session = Depends(get_db)):
     if current_admin_superadmin.deactivated_by_some_manager:
           raise HTTPException(status_code=403, detail="Un superadmin te ha desactivado. No puede cambiar roles")
     if not current_admin_superadmin.is_active:
           raise HTTPException(status_code=403, detail="Su usuario está desactivado. No puede cambiar roles")
     user = get_user_by_id(db, id)
     if not user:
            raise HTTPException(status_code=404, detail="El usuario no se encuentra registrado")
     if user.id ==  current_admin_superadmin.id :
          raise HTTPException(status_code=403, detail="No tiene autorización para cambiarse el rol a sí mismo")
 
     if user.role == "superadmin":
           raise HTTPException(status_code=403, detail="No tiene autorización para cambiarle el rol a un superadmin")
     if user.role =="admin" and  current_admin_superadmin.role == "admin":
           raise HTTPException(status_code=403, detail="No tiene autorización para cambiarle el rol a otro admin") 
     if user.role == "user" and current_admin_superadmin.role  == "admin" and data.new_role =="superadmin":
           raise HTTPException(status_code=403, detail="Los admin no pueden convertir un usuario a superadmin")
     
     change_user_role(db, user, data.new_role)

     return {"msg": "El rol se ha modificado con éxito"}
     
     
