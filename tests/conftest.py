import pytest
from tests.db_test import get_test_db
from crud.users.crud_post import create_user, create_user_for_tests
import schemas
import models
import bcrypt
from tests.users.functions.util import make_override_get_current_user
from utils.utils import get_current_user, get_current_admin, get_current_superadmin, get_current_admin_or_superadmin
from tests.client_config import client
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db


@pytest.fixture
def test_db():
    yield from get_test_db()
    


@pytest.fixture
def create_users_fixt(test_db):

    test_db.query(models.User).delete()
    test_db.commit() 

    

    users = [{"username": "username01","email": "fakeuser1@user.com", "password": "Password1!", "is_active": True, "deactivated_by_some_manager": False, "role" : "user"},
             {"username": "username02","email": "fakeuser2@user.com", "password": "Password2!",  "is_active": True, "deactivated_by_some_manager": False, "role": "user"},
             {"username": "username03","email": "fakeuser3@user.com", "password": "Password3!",  "is_active": True, "deactivated_by_some_manager": False, "role":"user"},
             {"username": "username04","email": "fakeuser4@user.com", "password": "Password4!",  "is_active": False, "deactivated_by_some_manager": False, "role":"user"},
             {"username": "username05","email": "fakeuser5@user.com", "password": "Password5!", "is_active": False, "deactivated_by_some_manager": True, "role": "user" },
             {"username": "username06","email": "fakeuser6@user.com", "password": "Password6!",  "is_active": True, "deactivated_by_some_manager": False, "role": "admin"   },
             {"username": "username07","email": "fakeuser7@user.com", "password": "Password7!",  "is_active": False, "deactivated_by_some_manager": True, "role": "admin"   },
             {"username": "username08","email": "fakeuser8@user.com", "password": "Password8!",  "is_active": True, "deactivated_by_some_manager": False, "role": "superadmin" },
             {"username": "username09","email": "fakeuser9@user.com", "password": "Password9!",  "is_active": True, "deactivated_by_some_manager": False, "role": "superadmin"}
                   ]
    
    for user in users :
        password_hashed = bcrypt.hashpw(user["password"].encode("utf-8"), bcrypt.gensalt() )
        create_user_for_tests(test_db, schemas.UserPostDataTests(username=user["username"], email = user["email"], password = password_hashed.decode("utf-8"), is_active = user["is_active"], deactivated_by_some_manager = user["deactivated_by_some_manager"], role = user["role"] ))

@pytest.fixture
def override_db(test_db):
          client.app.dependency_overrides[get_db] = lambda: test_db
          yield
          client.app.dependency_overrides.pop(get_db, None)

@pytest.fixture  
def override_fixture (test_db):  
   
    def override_function(dependency, username):
        client.app.dependency_overrides[dependency] = make_override_get_current_user(username,test_db)
    

    yield override_function
    client.app.dependency_overrides.pop(get_current_user, None)
    client.app.dependency_overrides.pop(get_current_admin, None)
    client.app.dependency_overrides.pop(get_current_superadmin, None)
    client.app.dependency_overrides.pop(get_current_admin_or_superadmin, None)    
