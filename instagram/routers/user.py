from fastapi import APIRouter, Depends
from routers.schemas import UserDisplay, UserBase
from sqlalchemy.orm.session import Session
from database.database import get_db
from database import db_user
from typing import List

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)

@router.get("",response_model=List[UserDisplay])
def retrieve_all(db: Session = Depends(get_db)):
    return db_user.retrieve_all(db)