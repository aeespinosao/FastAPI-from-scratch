from fastapi import APIRouter, Depends, UploadFile, File
from routers.schemas import PostBase, PostDisplay
from sqlalchemy.orm import Session
from database.database import get_db
from database import db_post
from typing import List
import shutil

router = APIRouter(
    prefix="/post",
    tags=["post"]
)

@router.post("", response_model=PostDisplay)
def create(request: PostBase, db: Session = Depends(get_db)):
    return db_post.create(request, db)

@router.get("", response_model=List[PostDisplay])
def retrieve(db: Session = Depends(get_db)):
    return db_post.get_all(db)

@router.get("/{id}", response_model=PostDisplay)
def retrieve_by_id(id: int, db: Session = Depends(get_db)):
    return db_post.get_by_id(id, db)

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return db_post.delete(id, db)

@router.post("/image")
def upload_image(image: UploadFile = File(...)):
    path = f"images/{image.filename}"
    
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {
        'filename': path
    }
