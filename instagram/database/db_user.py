from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from models.user import User
from utils.hashing import Hash
from fastapi.exceptions import HTTPException
from fastapi import status

def create_user(db: Session, request: UserBase):
    request.password = Hash.bcrypt(request.password)
    new_user = User(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return new_user

def retrieve_all(db: Session):
    return db.query(User).all()

def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user