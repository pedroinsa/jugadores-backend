from tests.client_config import client
from functions.util import make_override_get_current_user
from utils.utils import get_current_user, get_current_admin, get_current_superadmin, get_current_admin_or_superadmin
from tests.client_config import client
from tests.db_test import get_test_db
import pytest
import models

#change password successfully
def test_change_paswword_success(override_db, create_users_fixt, override_fixture):

   override_fixture(get_current_user, "username01")
   data_json = {"current_password": "Password1!", "new_password": "Passwordchange1!"}
   response = client.patch("/new-password", json=data_json)
   assert response.status_code == 200
   data = response.json()
   assert data["msg"] == "La contraseña se ha modificado con éxito"

#change password fails because the current password was not provided
def test_change_password_fails_no_current_password(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_user, "username01")
   data_json = {"current_password": "", "new_password": "Passwordchange1!"}
   response = client.patch("/new-password", json=data_json)
   assert response.status_code == 400
   data = response.json()
   assert data["detail"] == "Debe ingresar la contraseña actual"

# change password fails because the current password doesn't match the original one 
def test_change_password_fails_wrong_current_password(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_user, "username01")
   data_json = {"current_password": "Password1!distint", "new_password": "Passwordchange1!"}
   response = client.patch("/new-password", json=data_json)
   assert response.status_code == 400
   data = response.json()
   assert data["detail"] == "La contraseña que ha ingresado no coincide con la original"

# change password fails because the current and new passwords are the same
 
def test_change_password_fails_current_password_equal_new_password(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_user, "username01")
   data_json = {"current_password": "Password1!", "new_password": "Password1!"}
   response = client.patch("/new-password", json=data_json)
   assert response.status_code == 400
   data = response.json()
   assert data["detail"] == "La nueva contraseña no debe ser igual a la original"
# change password fails because the new password contains white spaces   
def test_change_password_fails_new_password_contains_white_spaces(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_user, "username01")
   data_json = {"current_password": "Password1!", "new_password": "Passwordchange1! "}
   response = client.patch("/new-password", json=data_json)
   assert response.status_code == 400
   data = response.json()
   assert data["detail"] == "La contraseña no puede tener espacios en blanco"
   
#change password fails because the new password has no  uppercase letter
def test_change_password_fails_new_password_has_no_uppercase_letter(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_user, "username01")
   data_json = {"current_password": "Password1!", "new_password": "passwordchange1!"}
   response = client.patch("/new-password", json=data_json)
   assert response.status_code == 400
   data = response.json()
   assert data["detail"] == "La contraseña debe tener al menos una letra mayúscula"


# User successfully deactivated .
def test_deactivate_user_successfully(override_db, create_users_fixt,override_fixture):
   override_fixture(get_current_user, "username01")
   response = client.patch("/user/deactivate")
   assert response.status_code == 200
   data = response.json()
   assert data["msg"] == "El usuario se ha desactivado"

#User deactivation fails because the user is already deactivated

def test_deactivate_fails_user_already_deactivated(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_user, "username04")
   response = client.patch("/user/deactivate")
   assert response.status_code == 400
   data = response.json()
   assert data["detail"] == "El usuario ya está desactivado"

#User deactivacion successfully
def test_reactivate_successfully(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_user, "username04")
   response = client.patch("/user/reactivate")
   assert response.status_code == 200
   data = response.json()
   assert data["msg"] == "El usuario se ha activado"
#User reactivation fails because the user is already activated
def test_reactivate_fails_user_already_activated(override_db,create_users_fixt, override_fixture):
   override_fixture(get_current_user, "username01")
   response = client.patch("/user/reactivate")
   assert response.status_code == 400
   data = response.json()
   assert data["detail"] == "El usuario ya se encuentra activado"

#Admin successfully deactivates User 
def test_admin_deactivate_user_successfully(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_admin, "username06")
   response = client.patch("/admin/users/2/deactivate")
   assert response.status_code == 200
   data = response.json()
   assert data["msg"] == "El usuario se ha desactivado"

#Admin can't desactivate the user because Admin is deactivated

def test_admin_cannot_deactivate_user(override_db, create_users_fixt, override_fixture):
   override_fixture = override_fixture(get_current_admin, "username07")
   response = client.patch("/admin/users/2/deactivate")
   assert response.status_code == 403
   data = response.json()
   assert data["detail"] == "Un superadmin te ha desactivado. Por favor comunicarse con gerencia"

#Admin can't deactivate the user because  the user doesn't exist
def test_admin_deactivate_user_doesnt_exist(override_db, create_users_fixt, override_fixture):
    override_fixture(get_current_admin, "username06")
    response = client.patch("/admin/users/91/deactivate")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "El usuario no se encuentra registrado"
#Admin can't deactivate themselves    
def test_admin_cannot_deactivate_themselves(override_db, create_users_fixt, override_fixture):
    override_fixture(get_current_admin, "username06")
    response = client.patch("/admin/users/6/deactivate")
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "El admin no puede modificarse a sí mismo desde esta ruta"

#Admin can't desactivate other Admin
def test_admin_cannot_deactivate_other_admin(override_db, create_users_fixt, override_fixture):
    override_fixture(get_current_admin, "username06")
    response = client.patch("/admin/users/7/deactivate")
    assert response.status_code == 403
    data  = response.json()
    assert data["detail"] ==  "No tiene autorización para modificar otro admin"

#Admin can't deactivate superadmin
def test_admin_cannot_deactivate_superadmin(override_db, create_users_fixt, override_fixture):
    override_fixture(get_current_admin, "username06")
    response = client.patch("/admin/users/8/deactivate")
    assert response.status_code == 403
    data  = response.json()
    assert data["detail"] ==  "No tiene autorización para modificar un superadmin"

#Admin can't deactivate the users because the User is alrededy deactivated
def test_admin_cannot_deactivate_user_is_already_deactivated(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_admin, "username06")
   response = client.patch(("/admin/users/4/deactivate"))
   assert response.status_code == 400
   data = response.json()
   assert data["detail"] == "El usuario ya está desactivado"

#Admin reactivate user successfully 
def test_admin_reactivate_user_successfully(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_admin, "username06")
   response = client.patch("/admin/users/4/reactivate")   
   assert response.status_code == 200
   data = response.json()
   assert data["msg"] == "El usuario se ha activado"

#Admin  can't reactivate the user because Admin is deactivated
def test_admin_can_not_reactivate_user(override_db, create_users_fixt, override_fixture):
   override_fixture = override_fixture(get_current_admin, "username07")
   response = client.patch("/admin/users/4/reactivate")
   assert response.status_code == 403
   data = response.json()
   assert data["detail"] == "Un superadmin te ha desactivado. Por favor comunicarse con gerencia"

#Admin can't reactivate the user because  the user doesn't exist
def test_admin_reactivate_user_doesnt_exist(override_db, create_users_fixt, override_fixture):
    override_fixture(get_current_admin, "username06")
    response = client.patch("/admin/users/91/reactivate")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "El usuario no se encuentra registrado"

#Admin can't reactivate themselves    
def test_admin_cannot_reactivate_themselves(override_db, create_users_fixt, override_fixture):
    override_fixture(get_current_admin, "username06")
    response = client.patch("/admin/users/6/reactivate")
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "El admin no puede modificarse a sí mismo desde esta ruta"

#Admin can't reactivate other Admin
def test_admin_cannot_reactivate_another_admin(override_db, create_users_fixt, override_fixture):
    override_fixture(get_current_admin, "username06")
    response = client.patch("/admin/users/7/reactivate")
    assert response.status_code == 403
    data  = response.json()
    assert data["detail"] ==  "No tiene autorización para modificar otro admin"
#Admin can't reactivate superadmin
def test_admin_cannot_reactivate_superadmin(override_db, create_users_fixt, override_fixture):
    override_fixture(get_current_admin, "username06")
    response = client.patch("/admin/users/8/reactivate")
    assert response.status_code == 403
    data  = response.json()
    assert data["detail"] ==  "No tiene autorización para modificar un superadmin"

#Admin can't reactivate the users because the User is alrededy activated
def test_admin_cannot_reactivate_user_is_already_activated(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_admin, "username06")
   response = client.patch(("/admin/users/2/reactivate"))
   assert response.status_code == 400
   data = response.json()
   assert data["detail"] == "El usuario ya se encuentra activado"

#Superadmin can deactivate user successfully
def test_superadmin_deactivate_user_successfully(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_superadmin, "username08")    
   response = client.patch("/superadmin/users/1/deactivate")
   assert response.status_code == 200
   data = response.json()
   assert data["msg"] == "El usuario se ha desactivado"
#Superadmin can't deactivate themselves   
def test_superadmin_cannot_deactivate_themselves(override_db, create_users_fixt, override_fixture) :
   override_fixture(get_current_superadmin, "username08") 
   response = client.patch("/superadmin/users/8/deactivate") 
   assert response.status_code == 403
   data = response.json()
   assert data["detail"] == "El superadmin no puede modificarse a sí mismo desde esta ruta"

#Superadmin can't deactivate other superadmin
def test_superadmin_cannot_deactivate_another_superadmin(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_superadmin, "username08")
   response = client.patch("/superadmin/users/9/deactivate")
   assert response.status_code == 403
   data = response.json()
   assert data["detail"] ==  "No tiene autorización para modificar otro superadmin"

 #Superadmin can reactivate the user 
def test_superadmin_can_reactivate_user(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_superadmin, "username08")
   response = client.patch("/superadmin/users/4/reactivate")
   assert response.status_code == 200
   data = response.json()
   assert data["msg"] == "El usuario se ha activado"
   

#Superadmin can't reactivate themselves   
def test_superadmin_cannot_reactivate_themselves(override_db, create_users_fixt, override_fixture) :
   override_fixture(get_current_superadmin, "username08") 
   response = client.patch("/superadmin/users/8/reactivate") 
   assert response.status_code == 403
   data = response.json()
   assert data["detail"] == "El superadmin no puede modificarse a sí mismo desde esta ruta"

#Superadmin can't deactivate other superadmin
def test_superadmin_cannot_reactivate_other_superadmin(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_superadmin, "username08")
   response = client.patch("/superadmin/users/9/reactivate")
   assert response.status_code == 403
   data = response.json()
   assert data["detail"] ==  "No tiene autorización para modificar otro superadmin"

# Admin can change a user's role

def test_admin_can_change_user_role(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_admin_or_superadmin, "username06")
   data_json = {"new_role": "admin"}
   response = client.patch("/manager/users/1/change-role", json=data_json)
   assert response.status_code == 200
   data = response.json()
   assert data["msg"] == "El rol se ha modificado con éxito"

#Admin can't change role because admin is deactivated by some manager
def test_admin_cannot_change_user_role_because_admin_is_deactivated_by_manager(override_db, create_users_fixt, override_fixture):
    override_fixture(get_current_admin_or_superadmin, "username07")
    data_json = {"new_role": "admin"}
    response = client.patch("/manager/users/1/change-role", json=data_json)
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Un superadmin te ha desactivado. No puede cambiar roles"

#Admin cannot change his own role
def test_admin_cannot_change_his_own_role(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_admin_or_superadmin, "username06")
   data_json = {"new_role": "superadmin"}
   response = client.patch("/manager/users/6/change-role",json=data_json)
   assert response.status_code == 403
   data = response.json()
   assert data["detail"] =="No tiene autorización para cambiarse el rol a sí mismo"
#Admin can't change superadmin's role   
def test_admin_cannot_change_superadmin_role(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_admin_or_superadmin, "username06")
   data_json = {"new_role": "admin"}
   response = client.patch("/manager/users/8/change-role", json=data_json)
   assert response.status_code == 403
   data = response.json()
   assert data["detail"] == "No tiene autorización para cambiarle el rol a un superadmin"
#Admin can't change another admin's role 
def test_admin_cannot_change_another_admin_role(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_admin_or_superadmin, "username06")
   data_json = {"new_role": "user"}
   response = client.patch("/manager/users/7/change-role", json=data_json)
   assert response.status_code == 403
   data = response.json()
   assert data["detail"] == "No tiene autorización para cambiarle el rol a otro admin"
# Admin can't change a user's role to 'superadmin
def test_admin_cannot_change_a_user_role_to_superadmin(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_admin_or_superadmin, "username06")
   data_json = {"new_role": "superadmin"}
   response = client.patch("/manager/users/1/change-role", json=data_json)
   assert response.status_code == 403
   data = response.json()
   assert data["detail"] == "Los admin no pueden convertir un usuario a superadmin"
#Superadmin can change a user's role to admin
def test_superadmin_can_change_a_user_role_to_admin(override_db, create_users_fixt, override_fixture):
    override_fixture(get_current_admin_or_superadmin, "username08")
    data_json = {"new_role": "admin"}
    response = client.patch("/manager/users/1/change-role", json=data_json)
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "El rol se ha modificado con éxito"
#Superadmin can change a user's role to superadmin
def test_superadmin_can_change_a_user_role_to_superadmin(override_db, create_users_fixt, override_fixture):
    override_fixture(get_current_admin_or_superadmin, "username08")
    data_json = {"new_role": "superadmin"}
    response = client.patch("/manager/users/1/change-role", json=data_json)
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "El rol se ha modificado con éxito"

#Superadmin can change a admin's role to superadmin 
def test_superadmin_can_change_a_admin_role_to_superadmin(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_admin_or_superadmin, "username08")
   data_json = {"new_role": "superadmin"}
   response = client.patch("/manager/users/6/change-role", json=data_json)
   assert response.status_code ==  200
   data = response.json()
   assert data["msg"] == "El rol se ha modificado con éxito"
#Superadmin can't change another superadmin's role
def test_superadmin_cannot_change_another_superadmin_role(override_db, create_users_fixt, override_fixture):
   override_fixture(get_current_admin_or_superadmin, "username08")
   data_json = {"new_role": "admin"}
   response = client.patch("/manager/users/9/change-role", json=data_json)
   assert response.status_code == 403
   data = response.json()
   assert data["detail"] == "No tiene autorización para cambiarle el rol a un superadmin"