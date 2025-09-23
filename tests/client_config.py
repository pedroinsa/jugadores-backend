
from fastapi.testclient import TestClient
from main import app
from models import User
import models
from utils.utils import get_current_user, get_current_admin, get_current_superadmin, get_current_admin_or_superadmin
from database import get_db
from tests.db_test import get_test_db, engine



models.Base.metadata.create_all(bind=engine)

client = TestClient(app)






