from tests.client_config import client
from fastapi import Response
import pytest

## test register successfully
def test_register_success(override_db):
    data_json= {"username": "fake_register", "email": "fake_email@fake.com", "password": "Fakepass1!"}
    response = client.post("/register", json= data_json)
    assert response.status_code == 201
    data = response.json()
    assert data["msg"]
    assert "access_token" in response.cookies
    #client.cookies.clear()
#Register test fails because the username already exists or is registered.
def test_register_username_exists(override_db):
    data_json= {"username": "username01", "email": "fake@user.com", "password": "Fakepass1!"}
    response = client.post("/register", json=data_json)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "El usuario o email ya se han registrado antes"

#Register test fails because the email already exists or is registered
def test_register_email_exists (override_db):
    data_json = {"username": "username10","email":"fakeuser1@user.com", "password": "Fakepass1!" }
    response = client.post("/register", json= data_json)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "El usuario o email ya se han registrado antes"
    
#Register test fails because the email format is invalid.
def test_register_email_invalid_format(override_db):
    data_json = {"username": "username10", "email": "@fakeuser.com", "password": "Fakepass1!"}
    response = client.post("/register", json=data_json)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Email con formato inválido"

#Register test fails because a field is missing in the JSON
def test_register_email_any_missing_field(override_db):
    data_json = {"username": "username10", "password": "Fakepass1!"}
    response = client.post("/register", json=data_json)
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["type"] == "missing"
    assert data["detail"][0]["msg"] == "Field required"
    assert data["detail"][0]["loc"][1] == "email"


#register test / logout 
def test_register_and_logout_successfully(override_db):
    data_json = {"username": "username10", "email": "fakeuser10@user.com", "password":"Fakepass1!"}
    response = client.post("/register", json=data_json)
    assert "access_token" in response.cookies
    #logout
    client.cookies.set("access_token", response.cookies.get("access_token"))
    response_logout = client.post("/logout")

    assert response_logout.status_code == 200
    assert "access_token" not in response_logout.cookies
    data = response_logout.json()
    assert data["msg"] == "Logout realizado con éxito"
    client.cookies.clear()

#Successful login test with username as credential
def test_login_successfully_with_username (override_db, create_users_fixt):
    data_json = {"user_credential": "username01", "password": "Password1!" }
    response = client.post("/login", json= data_json)
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "Login realizado con éxito"
    assert "access_token" in  response.cookies

#successful login test with a email as credential
def test_login_successfully_with_email (override_db, create_users_fixt):
    data_json = {"user_credential": "fakeuser1@user.com", "password": "Password1!"}
    response = client.post("/login", json=data_json)
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "Login realizado con éxito"

#Login test fails because the user doesn't exist.

def test_login_fail_user_doesnt_exists(override_db):
    data_json = {"user_credential": "username_fake", "password": "Password1!"}
    response = client.post("/login", json=data_json)
    assert response.status_code == 404
    data = response.json()
    assert data ["detail"] == "El usuario no existe en los registros"
#Login test fails because the user uses the wrong password.
def test_login_fail_wrong_password(override_db):
    data_json =  {"user_credential": "fakeuser1@user.com", "password": "WrongPassword1!"}
    response = client.post("/login", json =data_json)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "La contraseña no coincide"
