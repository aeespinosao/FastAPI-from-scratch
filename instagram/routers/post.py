from fastapi import APIRouter, Depends, status, UploadFile, File
from routers.schemas import PostDisplay, PostBase
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_post
from fastapi.exceptions import HTTPException
from typing import List
from random import choice
from string import ascii_letters
import shutil 

router = APIRouter(
    prefix="/post",
    tags=["post"]
)

image_url_type=["absolute", "relative"]

@router.post("", response_model=PostDisplay)
def create(request: PostBase, db: Session = Depends(get_db)):
    if  request.image_url_type not in image_url_type:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Parameter image_url_type can only take values 'absolute' or 'relative'"
        )
    return db_post.create(db, request)

@router.get("", response_model=List[PostDisplay])
def retrieve_all(db: Session = Depends(get_db)):
    return db_post.retrieve_all(db)

@router.post("/image", )
def upload_file(image: UploadFile = File(...)):
    rand_str = ''.join(choice(ascii_letters) for i in range(6))
    filename = f"_{rand_str}.".join(image.filename.rsplit(".", 1))
    path = f"images/{filename}"
    
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    return {"filename": path}