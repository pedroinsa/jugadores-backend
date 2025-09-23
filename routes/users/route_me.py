from fastapi import APIRouter,Depends
from utils.utils import get_current_user
import models





router = APIRouter()

@router.get("/me")
def get_me (user: models.User = Depends(get_current_user)):
    return user