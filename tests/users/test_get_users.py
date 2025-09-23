from tests.client_config import client
from models import User
####                                   tests de get                                ####


#get all users
def test_get_users (override_db, create_users_fixt):
    
    response = client.get("/users")
    assert response.status_code == 200     
    data = response.json()
    assert len(data) == 9

#get all active users
def test_get_users_actives(override_db, create_users_fixt):
    
    response =  client.get("/users/actives")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6

#get a user by username
def test_get_user_by_username(override_db, create_users_fixt):
    
    response =  client.get("/user/username?username=username01")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] ==  "username01"
    assert data["id"] == 1

#get a user by email
def test_get_user_by_email(override_db, create_users_fixt):
    response = client.get("/user/email?email=fakeuser3@user.com") 
    assert response.status_code == 200
    data = response.json()
    assert data["email"]  == "fakeuser3@user.com"
    assert data["username"] == "username03"
    assert data["id"] == 3  

#get a user bye id
def test_get_user_by_id(override_db, create_users_fixt):
    response = client.get("/user/2")
    assert response.status_code == 200
    data = response.json()
    assert data["username"]  == "username02"
    assert data ["email"] == "fakeuser2@user.com"


## Test that there is no match when passing a non-existent username.
def test_get_users_by_username_non_existent_username (override_db, create_users_fixt):
    response = client.get("/users/username?username=name_false")
    assert response.status_code == 200
    data = response.json()
    assert data == []
## Test with a non-existent ID in the database
def test_get_user_by_id_non_existent_id (override_db, create_users_fixt):
    
    response = client.get("/user/99")
    assert response.status_code == 404 
    data = response.json()
    assert data["detail"] == "No existe un usuario con ese ID"
##test with a non - existent username in the database
def test_get_user_by_non_existent_username():
    response = client.get("/user/username?username=username99")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No existe un usuario con ese username"

    

      
 

