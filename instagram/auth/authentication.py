from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database.database import get_db
from sqlalchemy.orm.session import Session
from database import db_user
from utils.hashing import Hash
from fastapi.exceptions import HTTPException
from auth.oauth2 import create_access_token

router = APIRouter(
    tags=["authentication"]
)

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db_user.get_user_by_username(db, request.username)
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect credentials")
    
    token = create_access_token(data={"username": user.username})
    
    return {
        "token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }