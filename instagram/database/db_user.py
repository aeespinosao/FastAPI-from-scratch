from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from models.user import User
from utils.hashing import Hash

def create_user(db: Session, request: UserBase):
    request.password = Hash.bcrypt(request.password)
    new_user = User(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return new_user

def retrieve_all(db: Session):
    return db.query(User).all()