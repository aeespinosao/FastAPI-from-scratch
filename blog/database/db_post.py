from routers.schemas import PostBase
from sqlalchemy.orm import Session
from datetime import datetime
from database.models import DbPost
from fastapi import HTTPException, status

def create(request: PostBase, db: Session):
    new_post = DbPost(
        **request.dict(),
        timestamp = datetime.now()
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all(db: Session):
    return db.query(DbPost).all()

def get_by_id(id: int, db: Session):
    return db.query(DbPost).filter(DbPost.id == id).first()

def delete(id: int, db: Session):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
    db.delete(post)
    db.commit()
    return 'ok'