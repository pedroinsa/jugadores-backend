from fastapi import HTTPException
import checkers.checkers as checkers
import pytest

#test check username
def test_checker_username():
      username = "username"
      assert checkers.check_username(username) == "username" 

def test_checker_username_capital_letters():
      username = "USERNAME"
      assert checkers.check_username(username) == "username"

def test_checker_username_white_space():
      username = "username "
      with pytest.raises(HTTPException) as exc:
          checkers.check_username(username)
      assert exc.value.detail  == "Username no debe tener espacios"    

def test_checker_username_no_repeat():
      username = "usernameee"
      with pytest.raises(HTTPException) as exc:
            checkers.check_username(username)
      assert exc.value.status_code == 400
      assert exc.value.detail == "Los caracteres no pueden repetirse 3 veces o más"
def test_checker_username_invalid_character():
      username = "username+"
      with pytest.raises(HTTPException) as exc:
           checkers.check_username(username)
      assert exc.value.detail == "Tiene caracteres incorrectos"      
      
def test_checker_username_restricted_word ():
      username = "user"
      with  pytest.raises(HTTPException) as exc:
            checkers.check_username(username)
      assert exc.value.detail == "Prohibido uso de palabras reservadas"      
   
#test check email
def test_checker_email():
      email = "username@user.com"  
      assert checkers.check_email(email) == "username@user.com" 

def test_checker_email_capital_letter():
      email = "USERNAME@USER.COM"
      assert checkers.check_email(email) == "username@user.com" 

def test_checker_email_no_symbol():
      email = "usernameuser.com"
      with pytest.raises(HTTPException) as exc :
            checkers.check_email(email)
      assert exc.value.status_code == 400
      assert exc.value.detail == "Debe contener un @"       

def test_checker_email_white_space():
      email = "username@user.com "
      with pytest.raises(HTTPException) as exc:
            checkers.check_email(email)
      assert exc.value.detail == "Email no debe tener espacios"       
def test_checker_email_valid_format():
      email = "@usernameuser.com"
      with pytest.raises(HTTPException) as exc:
            checkers.check_email(email)
      assert exc.value.detail == "Email con formato inválido"
      
def test_checker_email_starts_ok ():
      email = "+username@user.com"
      with pytest.raises(HTTPException) as exc:
          checkers.check_email(email)
      assert exc.value.detail  == "Email debe comenzar con letras o números"       

def test_checker_email_domain_ok():
      email = "username@.user.com"
      with pytest.raises(HTTPException) as exc:
            checkers.check_email(email)
      assert exc.value.status_code == 400      
      assert exc.value.detail == "El dominio del email debe comenzar con letras"     

def test_checker_email_no_repeat():
      email =  "username@uuuuser.com"
      with pytest.raises(HTTPException) as exc :
            checkers.check_email(email)
      assert exc.value.detail == "No puedes repetir tantos caracteres seguidos"      

def test_checker_email_no_dots():
      email = "username@use..er.com"
      with pytest.raises(HTTPException) as exc:
            checkers.check_email(email)
      assert exc.value.detail == "El dominio no puede tener puntos consecutivos"     
    

def test_checker_email_right_domain():
      email = "username@user.-us.com"
      with pytest.raises(HTTPException) as exc:
            checkers.check_email(email)
      assert exc.value.detail == "Dominio con formato inválido"

#check password

def test_checker_password_output_ok ():
      password = "Password1!"
      assert checkers.check_password(password) == "Password1!"

def test_checker_password_white_space() :
      password = "Pass word1"
      with pytest.raises(HTTPException) as exc:
            checkers.check_password(password)
      assert exc.value.detail == "La contraseña no puede tener espacios en blanco"       
def test_checker_password_max_length ():
      password = "String_length_mayor_a_25!!"
      with pytest.raises(HTTPException) as exc:
            checkers.check_password(password)
      assert exc.value.detail  == "La contraseña debe tener entre 8 y 25 caracteres"      
def test_checker_password_min_length ():
      password = "Stg1!"
      with pytest.raises(HTTPException) as exc:
            checkers.check_password(password)
      assert exc.value.detail  == "La contraseña debe tener entre 8 y 25 caracteres"            
def test_checker_password_any_lowercase_letter():
       password = "PASSWORD1!"
       with pytest.raises(HTTPException) as exc:
             checkers.check_password(password)
       assert exc.value.detail == "La contraseña debe tener al menos una letra minúscula"       

def test_checker_password_any_capital_letter():
       password = "password1!"
       with pytest.raises(HTTPException) as exc:
             checkers.check_password(password)
       assert exc.value.detail == "La contraseña debe tener al menos una letra mayúscula"  

def test_checker_password_any_number ():
       password = "Password!"
       with pytest.raises(HTTPException) as exc:
             checkers.check_password(password)
       assert exc.value.detail == "La contraseña debe tener al menos un número"       

def test_checker_password_any_special_character():
      password = "Password1"
      with pytest.raises(HTTPException) as exc:
            checkers.check_password(password)
      assert exc.value.detail == "La contraseña debe tener al menos un carácter especial"