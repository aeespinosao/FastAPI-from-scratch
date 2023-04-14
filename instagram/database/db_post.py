from routers.schemas import PostBase
from sqlalchemy.orm.session import Session
from models.post import Post
from datetime import datetime
from fastapi.exceptions import HTTPException
from fastapi import status

def create(db: Session, request: PostBase):
    print(request.dict())
    new_post = Post(
        **request.dict(),
        timestamp=datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def retrieve_all(db: Session):
    return db.query(Post).all()

def delete(db: Session, id: int, user_id: int):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only post creator can delete post")
    
    db.delete(post)
    db.commit()
    return 'ok'