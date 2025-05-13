from fastapi import APIRouter
from models import PasswordRequest  
from validator import validate_password  

router = APIRouter()

@router.post("/verify-password/")
def verify_password(data: PasswordRequest):
    return validate_password(data.password)
